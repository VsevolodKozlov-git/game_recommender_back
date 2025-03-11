from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Game(Base):
    __tablename__ = "game"
    __table_args__ = {"schema": "public"}

    id_game = Column(Integer, primary_key=True)
    gamename = Column(String(50), index=True, nullable=False)
    steam_link = Column(String(512), index=True, nullable=False)
    questions = relationship("Question", back_populates="game")