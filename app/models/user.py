from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "public"}

    id_user = Column(Integer, primary_key=True)
    username = Column(String(50), index=True, nullable=False)
    password = Column(String(250), nullable=False)
