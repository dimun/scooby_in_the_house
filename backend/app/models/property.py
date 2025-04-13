from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.sql import func

from app.db import Base


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(512), unique=True, index=True)
    title = Column(String(256), nullable=True)
    price = Column(Float, nullable=True)
    rooms = Column(Integer, nullable=True)
    bathrooms = Column(Integer, nullable=True)
    surface = Column(Float, nullable=True)
    surface_unit = Column(String(10), nullable=True, default="m²")
    city = Column(String(128), nullable=True)
    region = Column(String(128), nullable=True)
    description = Column(Text, nullable=True)
    property_type = Column(String(128), nullable=True)
    image_urls = Column(JSON, nullable=True, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now()) 