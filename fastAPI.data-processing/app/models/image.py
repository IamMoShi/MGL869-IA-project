from datetime import datetime

from app.models.base import Base
from sqlalchemy import Column, DateTime, Integer, String


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False, unique=True)
    category = Column(Integer)
    attribution_method = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
