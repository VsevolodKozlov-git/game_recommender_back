from pydantic import BaseModel, Field
from typing import Optional, List


# Question Schemas
class QuestionBase(BaseModel):
    pass

class QuestionCreate(QuestionBase):
    survey_id: int  # This will be used to associate the question with a survey
    game_id: int  # This will be used to associate the question with a game

class QuestionUpdate(QuestionBase):
    pass

class QuestionRead(QuestionBase):
    question_id: int
    survey_id: int
    game_id: int
    survey_name: Optional[str] = None
    game_name: Optional[str] = None

    class Config:
        from_attributes = True