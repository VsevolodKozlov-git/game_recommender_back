
from fastapi import APIRouter, Depends
from app.schemas.recommender import GetGameRequest, GetGameResponse, UserResponseRequest
from app.models.user import User
from app.models.game import Game
from app.models.reaction import Reaction
from app.core.auth import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.db.session import get_session
import random

router = APIRouter(prefix="/recommender")


class GameRecommendationsModel:
    def __init__(self, top_k=10):
        self.model = torch.load('/content/drive/My Drive/recom/recom_model_30k.pt', map_location='cpu', weights_only=False)
        #self.model = model

        self.num_items = self.model.item_embeddings.weight.shape[0] - 1
        self.max_seq_length = self.model.position_embeddings.weight.shape[0]
        self.model.eval()

    def sanitize_sequence(self, sequence, num_items):
        """Replace invalid item IDs with 0 (padding)."""
        if len(sequence) > self.max_seq_length:
                sequence = sequence[-self.max_seq_length:]
        else:
                pad = [0] * (self.max_seq_length - len(sequence))
                pad.extend(sequence)
                sequence = pad

        return [item if 0 <= item <= num_items else 0 for item in sequence]

    def get_recommendation(self, sequence, top_k=10, device='cpu'):
        sequence = self.sanitize_sequence(sequence, self.num_items)
        self.model.to(device)
        input_tensor = torch.tensor([sequence], dtype=torch.long, device=device)  # Shape: [1, seq_len]

        with torch.no_grad():
            logits = self.model(input_tensor)

        last_position_logits = logits[0, -1, :]

        valid_items_mask = torch.ones(self.num_items + 1, dtype=torch.bool, device=device)
        valid_items_mask[0] = False

        seen_items = torch.tensor(list(set(sequence)), device=device)
        valid_items_mask[seen_items] = False

        valid_logits = last_position_logits[valid_items_mask]
        valid_item_ids = torch.arange(1, self.num_items + 1, device=device)[valid_items_mask[1:]]  # IDs start at 1

        top_scores, top_indices = torch.topk(valid_logits, k=10)
        top_item_ids = valid_item_ids[top_indices].cpu().numpy().tolist()

        return top_item_ids





@router.post("/get_game", response_model=GetGameResponse)
async def get_game(params: GetGameRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    list_liked_games = await db.execute(
        select(
            Game.id_game
        ).join(Reaction).where(
            (Reaction.id_user == user.id_user) &
            (or_(
                Reaction.has_played == True,
                Reaction.want_to_play == True
            ))
        )
    )


    list_disliked_games = await db.execute(
            select(
                Game.id_game
            ).join(Reaction).where(
                (Reaction.id_user == user.id_user) &
                (Reaction.want_to_play == False)
            )
        )
    
    list_to_recommend = await db.execute(
         select(
              Game.id_game,
              Game.title,
              Game.header_image
         ).where(
              (Game.short_description != 'string') &
            (Game.header_image != 'string') &
            (Game.positive_ratio >= 50)
         )
    )

    sequence = [row.id_game for row in list_liked_games.all()]
    false_sequence = [row.id_game for row in list_disliked_games.all()]

    # recomModel = GameRecommendationsModel()
    # top_item_ids = recomModel.get_recommendation(sequence)

    recommendation = 0

    for id in list_to_recommend:
        if id[0] in false_sequence or id[0] in sequence:
            continue
        recommendation = id
        break

    return GetGameResponse(id_game=recommendation[0])


@router.post("/user_response")
async def user_response(data: UserResponseRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    list_liked_games = await db.execute(
        select(
            Game.id_game
        ).join(Reaction).where(
            (Reaction.id_user == user.id_user) &
            (or_(
                Reaction.has_played == True,
                Reaction.want_to_play == True
            ))
        )
    )

    list_disliked_games = await db.execute(
            select(
                Game.id_game
            ).join(Reaction).where(
                (Reaction.id_user == user.id_user) &
                (Reaction.want_to_play == False)
            )
        )
    
    list_to_recommend = await db.execute(
         select(
              Game.id_game,
              Game.title,
              Game.header_image
         )
    )

    sequence = [row.id_game for row in list_liked_games.all()]
    false_sequence = [row.id_game for row in list_disliked_games.all()]

    # recomModel = GameRecommendationsModel()
    # top_item_ids = recomModel.get_recommendation(sequence)

    recommendation = 0

    for id in list_to_recommend:
        while id in false_sequence or id in sequence:
            continue
        recommendation = id
        break
         

    return GetGameResponse(id_game=recommendation[0])