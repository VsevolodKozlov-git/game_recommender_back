from sqlalchemy import Column, Integer, String, Date, Boolean, Numeric
from sqlalchemy.orm import relationship
from app.db.base_class import Base

from app.db.base_class import Base


class Game(Base):
    __tablename__ = "game"
    __table_args__ = {"schema": "public"}

    id_game = Column(Integer, primary_key=True)  # Maps to CSV's "app_id"
    title = Column(String(1000), nullable=True)
    header_image = Column(String(1000), nullable=True)
    date_release = Column(Date)
    win = Column(Boolean)
    mac = Column(Boolean)
    linux = Column(Boolean)
    rating = Column(String(2000))  # New column for "Very Positive", "Positive", etc.
    positive_ratio = Column(Integer)
    user_reviews = Column(Integer)
    price_final = Column(Numeric(1000, 2))
    short_description = Column(String(5000))

    reactions = relationship("Reaction", back_populates="game")