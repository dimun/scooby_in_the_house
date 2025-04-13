from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List
from datetime import datetime


class PropertyBase(BaseModel):
    url: HttpUrl
    title: Optional[str] = None
    price: Optional[float] = None
    rooms: Optional[int] = None
    bathrooms: Optional[int] = None
    surface: Optional[float] = None
    surface_unit: Optional[str] = "m²"
    city: Optional[str] = None
    region: Optional[str] = None
    property_type: Optional[str] = None
    image_urls: Optional[List[HttpUrl]] = None


class PropertyCreate(PropertyBase):
    pass


class PropertyResponse(PropertyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ScraperRequest(BaseModel):
    city: str
    region: str
    property_types: Optional[List[str]] = Field(["casas"], description="List of property types to search for (e.g., 'casas', 'apartamentos', 'fincas', etc.)")
    max_pages: Optional[int] = Field(5, description="Maximum number of pages to scrape", ge=1, le=100) 