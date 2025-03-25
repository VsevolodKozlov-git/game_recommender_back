from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Question(Base):
    __tablename__ = "question"
    __table_args__ = {"schema": "public"}

    question_id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, ForeignKey('public.survey.survey_id'), nullable=False)

    # Relationships
    survey = relationship("Survey", back_populates="questions")
