from pydantic import BaseModel, validator, ValidationError

class ReactionBase(BaseModel):
    id_game: int
    has_played: bool
    rating: int | None = None
    want_to_play: bool | None = None

    @validator('rating')
    def validate_rating(cls, v, values):
        if values.get('has_played') and (v is None or not (1 <= v <= 10)):
            raise ValueError('Rating must be between 1-10 for played games')
        return v

    @validator('want_to_play')
    def validate_want_to_play(cls, v, values):
        if not values.get('has_played') and v is None:
            raise ValueError('Want to play must be specified for unplayed games')
        return v

class ReactionResponse(ReactionBase):
    reaction_id: int
    id_user: int

class UserGamesResponse(BaseModel):
    id_game: int