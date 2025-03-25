from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.db.session import get_session
from app.models import Reaction, Game, User
from app.schemas.reaction import ReactionBase, ReactionResponse, UserGamesResponse
from app.core.auth import get_current_user

router = APIRouter(prefix="/reaction")

@router.post("/", response_model=ReactionResponse)
async def create_update_reaction(
    reaction: ReactionBase,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    # Check if reaction exists
    result = await db.execute(
        select(Reaction).where(
            (Reaction.id_user == user.id_user) &
            (Reaction.id_game == reaction.id_game)
        )
    )
    existing = result.scalar_one_or_none()

    # Create or update reaction
    if existing:
        existing.has_played = reaction.has_played
        existing.rating = reaction.rating
        existing.want_to_play = reaction.want_to_play
    else:
        reaction_dict = reaction.dict()
        reaction_dict.pop('id_game', None)  # Remove id_game from the dictionary
        new_reaction = Reaction(
            id_game=reaction.id_game,
            id_user=user.id_user,
            **reaction_dict
        )
        db.add(new_reaction)

    await db.commit()
    await db.refresh(new_reaction if not existing else existing)
    return existing if existing else new_reaction

@router.get("/me", response_model=list[UserGamesResponse])
async def get_user_games(
    db: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(
            Game.id_game,
            Game.title,
            Game.header_image,
            Reaction.has_played,
            Reaction.rating,
            Reaction.want_to_play
        ).join(Reaction).where(
            (Reaction.id_user == user.id_user) &
            (or_(
                Reaction.has_played == True,
                Reaction.want_to_play == True
            ))
        )
    )
    
    return [UserGamesResponse(
        id_game=row.id_game,
    ) for row in result.all()]