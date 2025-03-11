from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_session
from app.models.game import Game  # Adjust the import according to your project structure
from app.schemas.game import GameCreate, GameUpdate, GameRead  # Define these schemas

router = APIRouter(prefix="/games")

@router.post("/", response_model=GameRead)
async def create_game(game: GameCreate, db: AsyncSession = Depends(get_session)):
    new_game = Game(**game.dict())
    db.add(new_game)
    await db.commit()
    await db.refresh(new_game)
    return new_game

@router.get("/{game_id}", response_model=GameRead)
async def get_game(game_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Game).where(Game.id_game == game_id))
    game = result.scalar_one_or_none()
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@router.get("/", response_model=list[GameRead])
async def list_games(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Game))
    games = result.scalars().all()
    return games

@router.put("/{game_id}", response_model=GameRead)
async def update_game(game_id: int, game: GameUpdate, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Game).where(Game.id_game == game_id))
    db_game = result.scalar_one_or_none()
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    for key, value in game.dict(exclude_unset=True).items():
        setattr(db_game, key, value)
    await db.commit()
    await db.refresh(db_game)
    return db_game

@router.delete("/{game_id}", response_model=GameRead)
async def delete_game(game_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Game).where(Game.id_game == game_id))
    db_game = result.scalar_one_or_none()
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    await db.delete(db_game)
    await db.commit()
    return db_game