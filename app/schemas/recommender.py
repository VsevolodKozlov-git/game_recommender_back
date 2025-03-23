from pydantic import BaseModel, conint

from typing import Optional, List


class RangeFloat(BaseModel):
    min_value: Optional[float]
    max_value: Optional[float]


class RangeInt(BaseModel):
    min_value: Optional[int]
    max_value: Optional[int]

class GetGameRequest(BaseModel):
    price_final: Optional[RangeFloat] = None
    user_reviews: Optional[RangeInt]  = None
    positive_ratio: Optional[RangeInt] = None
    linux: Optional[bool] = None
    mac: Optional[bool] = None
    
class UserResponseItem(BaseModel):
    id_game: int
    is_played: bool
    like_to_play: Optional[bool]
    rating: Optional[conint(ge=0, le=10)]


class UserResponseRequest(BaseModel):
    user_response: List[UserResponseItem]
    
class GetGameResponse(BaseModel):
    id_game: int
