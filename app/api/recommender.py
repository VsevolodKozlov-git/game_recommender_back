
from fastapi import APIRouter, Depends
from app.schemas.recommender import GetGameRequest, GetGameResponse, UserResponseRequest
from app.models.user import User
from app.core.auth import get_current_user

router = APIRouter(prefix="/recommender")




@router.post("/get_game", response_model=GetGameResponse)
def get_game(params: GetGameRequest, user: User = Depends(get_current_user)):
    # todo
    return GetGameResponse(id_game=1234)


@router.post("/user_response")
def user_response(data: UserResponseRequest, user: User = Depends(get_current_user)):
    # todo
    return {"msg": "ok"}