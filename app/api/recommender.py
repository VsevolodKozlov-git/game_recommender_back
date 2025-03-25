
from fastapi import APIRouter, Depends
from app.schemas.recommender import GetGameRequest, GetGameResponse, UserResponseRequest
from app.models.user import User
from app.core.auth import get_current_user
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence

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
def get_game(params: GetGameRequest, user: User = Depends(get_current_user)):
    # todo
    return GetGameResponse(id_game=10)


@router.post("/user_response")
def user_response(data: UserResponseRequest, user: User = Depends(get_current_user)):
    # todo
    return {"msg": "ok"}