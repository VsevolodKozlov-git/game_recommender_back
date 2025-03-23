from pydantic import BaseModel, Field
from typing import Optional

# class GameBase(BaseModel):
#     gamename: str = Field(..., min_length=1, max_length=50)
#     steam_link: str = Field(..., min_length=1, max_length=512)  # Ensure the URL is valid

# class GameCreate(GameBase):
#     pass

# class GameUpdate(GameBase):
#     gamename: Optional[str] = Field(None, min_length=1, max_length=50)
#     steam_link: Optional[str] = None

# class GameRead(GameBase):
#     id_game: int

#     class Config:
#         orm_mode = True

class GameInfoResponse(BaseModel):
    title: str
    header_image: str  # URL to image
    short_description: str
