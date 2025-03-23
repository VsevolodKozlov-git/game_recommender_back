from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_session
from app.models.game import Game
from app.models.user import User
from app.schemas.game import GameInfoResponse  
from app.core.auth import get_current_user

router = APIRouter(prefix="/game")

# @router.post("/", response_model=GameRead)
# async def create_game(game: GameCreate, db: AsyncSession = Depends(get_session)):
#     new_game = Game(**game.dict())
#     db.add(new_game)
#     await db.commit()
#     await db.refresh(new_game)
#     return new_game

next_response = 0
@router.get("/{game_id}", response_model=GameInfoResponse)
async def get_game(game_id: int, db: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    # todo
    # result = await db.execute(select(Game).where(Game.id_game == game_id))
    # game = result.scalar_one_or_none()
    # if game is None:
    #     raise HTTPException(status_code=404, detail="Game not found")
    global next_response
    
    description0 = """Factorio - это игра, в которой вы строите фабрики и поддерживаете их работу.

Вы будете добывать ресурсы, исследовать новые технологии, создавать инфраструктуру, автоматизировать производство и сражаться с врагами.

На начальном этапе игры Вы будете вручную рубить деревья, добывать руду и создавать простые манипуляторы и транспортные конвейеры, но через некоторое время Вы, наконец, сможете подняться до энергетической индустрии с огромными солнечными фермами, перегонкой и переработкой нефти, построить роботов и развернуть логистическую сеть, настроенную для Ваших потребностей в ресурсах.
    """
    response0 = GameInfoResponse(
        title="Factorio",
        header_image="https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/427520/header.jpg?t=1730307306",
        short_description=description0,
    )
    
    description1 = """Игра в жанре выживание, в которой вам предстоит исследовать огромный фэнтезийный мир, пропитанный скандинавской мифологией и культурой викингов."""
    response1 = GameInfoResponse(
        title="Valheim",
        header_image="https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/892970/header.jpg?t=1738051073",
        short_description=description1,
    )
    response = [response0, response1][next_response]
    
 
    next_response = (next_response+1) % 2
    
    return response

# @router.get("/", response_model=list[GameRead])
# async def list_games(db: AsyncSession = Depends(get_session)):
#     result = await db.execute(select(Game))
#     games = result.scalars().all()
#     return games

# @router.put("/{game_id}", response_model=GameRead)
# async def update_game(game_id: int, game: GameUpdate, db: AsyncSession = Depends(get_session)):
#     result = await db.execute(select(Game).where(Game.id_game == game_id))
#     db_game = result.scalar_one_or_none()
#     if db_game is None:
#         raise HTTPException(status_code=404, detail="Game not found")
#     for key, value in game.dict(exclude_unset=True).items():
#         setattr(db_game, key, value)
#     await db.commit()
#     await db.refresh(db_game)
#     return db_game

# @router.delete("/{game_id}", response_model=GameRead)
# async def delete_game(game_id: int, db: AsyncSession = Depends(get_session)):
#     result = await db.execute(select(Game).where(Game.id_game == game_id))
#     db_game = result.scalar_one_or_none()
#     if db_game is None:
#         raise HTTPException(status_code=404, detail="Game not found")
#     await db.delete(db_game)
#     await db.commit()
#     return db_game