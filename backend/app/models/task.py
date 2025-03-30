from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.sql import func

from app.db import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String(8), primary_key=True, index=True)
    city = Column(String(128), nullable=False)
    region = Column(String(128), nullable=False)
    property_type = Column(String(256), nullable=False)
    max_pages = Column(Integer, nullable=False, default=5)
    status = Column(String(20), nullable=False, default="pending")  # pending, running, completed, failed
    properties_found = Column(Integer, nullable=True)
    error = Column(Text, nullable=True)
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True), nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    cmetadata = Column(JSON, nullable=True)