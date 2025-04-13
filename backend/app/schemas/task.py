from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime


class TaskBase(BaseModel):
    city: str
    region: str
    property_type: str
    max_pages: int


class TaskCreate(TaskBase):
    id: str
    status: str = "pending"


class TaskUpdate(BaseModel):
    status: Optional[str] = None
    properties_found: Optional[int] = None
    error: Optional[str] = None
    end_time: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None


class TaskResponse(TaskBase):
    id: str
    status: str
    properties_found: Optional[int] = None
    error: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    cmetadata: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)


class ScrapingLogResponse(BaseModel):
    logs: List[str]


class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
    total: int 