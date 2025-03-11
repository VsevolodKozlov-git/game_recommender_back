from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from .question import QuestionRead

# Survey Schemas
class SurveyBase(BaseModel):
    survey_name: str = Field(..., min_length=1, max_length=50)

class SurveyCreate(SurveyBase):
    pass

class SurveyUpdate(SurveyBase):
    survey_name: Optional[str] = Field(None, min_length=1, max_length=50)

class SurveyRead(SurveyBase):
    survey_id: int
    questions: List[QuestionRead] = []

    model_config = ConfigDict(from_attributes=True)