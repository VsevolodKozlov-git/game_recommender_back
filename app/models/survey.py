from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Survey(Base):
    __tablename__ = "survey"
    __table_args__ = {"schema": "public"}

    survey_id = Column(Integer, primary_key=True)
    survey_name = Column(String(50), index=True, nullable=False)

    # Relationships
    questions = relationship("Question", back_populates="survey")