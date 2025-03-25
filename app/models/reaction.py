from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Reaction(Base):
    __tablename__ = "reaction"
    __table_args__ = {"schema": "public"}

    reaction_id = Column(Integer, primary_key=True)
    id_game = Column(Integer, ForeignKey("public.game.id_game"), nullable=False)
    id_user = Column(Integer, ForeignKey("public.user.id_user"), nullable=False)
    has_played = Column(Boolean, nullable=False)
    rating = Column(Integer, nullable=True)
    want_to_play = Column(Boolean, nullable=True)

    # Relationships
    game = relationship("Game", back_populates="reactions")
    user = relationship("User", back_populates="reactions")