from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.property import Property
from app.schemas.property import PropertyResponse
from app.db.repositories import PropertyRepository

class PropertyUseCases:
    def __init__(self, db: Session):
        self.db = db
        self.property_repo = PropertyRepository(db)
        
    def get_properties(
        self,
        city: Optional[str] = None,
        region: Optional[str] = None,
        property_type: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_rooms: Optional[int] = None,
        min_bathrooms: Optional[int] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[Property]:
        """
        Get properties with optional filtering
        """
        return self.property_repo.get_properties_with_filters(
            city=city,
            region=region,
            property_type=property_type,
            min_price=min_price,
            max_price=max_price,
            min_rooms=min_rooms,
            min_bathrooms=min_bathrooms,
            skip=skip,
            limit=limit
        )
        
    def get_property_stats(self):
        """
        Get statistics about properties in the database
        """
        total_count = self.property_repo.get_property_count()
        city_stats = self.property_repo.get_property_count_by_city()
        price_stats = self.property_repo.get_avg_price_by_city()
        
        return {
            "total_properties": total_count,
            "by_city": city_stats,
            "avg_prices": price_stats
        } 