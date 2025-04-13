from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Dict, Any, Optional
import logging

from app.models.property import Property
from app.schemas.property import PropertyCreate

logger = logging.getLogger(__name__)


class PropertyRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_properties_with_filters(
        self,
        city: Optional[str] = None,
        region: Optional[str] = None,
        property_type: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_rooms: Optional[int] = None,
        min_bathrooms: Optional[int] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> List[Property]:
        """
        Get properties from the database with optional filtering
        """
        query = self.db.query(Property)

        if city:
            query = query.filter(Property.city.ilike(f"%{city}%"))
        if region:
            query = query.filter(Property.region.ilike(f"%{region}%"))
        if property_type:
            query = query.filter(Property.property_type.ilike(f"%{property_type}%"))
        if min_price:
            query = query.filter(Property.price >= min_price)
        if max_price:
            query = query.filter(Property.price <= max_price)
        if min_rooms:
            query = query.filter(Property.rooms >= min_rooms)
        if min_bathrooms:
            query = query.filter(Property.bathrooms >= min_bathrooms)

        # Order by creation date descending
        query = query.order_by(Property.created_at.desc())

        # Paginate results
        properties = query.offset(skip).limit(limit).all()

        return properties

    def get_property_count(self) -> int:
        """Get total count of properties"""
        return self.db.query(Property).count()

    def get_property_count_by_city(self) -> List[Dict[str, Any]]:
        """Get property counts grouped by city"""
        city_stats = (
            self.db.query(Property.city, self.db.func.count(Property.id).label("count"))
            .group_by(Property.city)
            .all()
        )

        return [{"city": city, "count": count} for city, count in city_stats]

    def get_avg_price_by_city(self) -> List[Dict[str, Any]]:
        """Get average prices by city"""
        price_stats = (
            self.db.query(
                Property.city, self.db.func.avg(Property.price).label("avg_price")
            )
            .group_by(Property.city)
            .all()
        )

        return [
            {"city": city, "avg_price": avg_price} for city, avg_price in price_stats
        ]

    def check_existing_property_urls(self, urls: List[str]) -> Dict[str, Property]:
        """
        Get existing properties by URLs

        Returns a dictionary mapping URLs to property objects
        """
        existing_properties: Dict[str, Property] = {}
        if not urls:
            return existing_properties

        for existing in self.db.query(Property).filter(Property.url.in_(urls)).all():
            existing_properties[str(existing.url)] = existing

        return existing_properties

    def update_property(
        self, property_obj: Property, property_data: Dict[str, Any]
    ) -> None:
        """Update an existing property with new data"""
        for key, value in property_data.items():
            if hasattr(property_obj, key):
                if key == "url" and value is not None:
                    setattr(property_obj, key, str(value))
                elif key == "image_urls" and value is not None:
                    setattr(property_obj, key, [str(url) for url in value])
                else:
                    setattr(property_obj, key, value)

    def create_property(self, property_data: Dict[str, Any]) -> Property:
        """Create a new property from data"""

        new_property = Property(
            url=str(property_data.get("url")),
            title=property_data.get("title"),
            price=property_data.get("price"),
            rooms=property_data.get("rooms"),
            bathrooms=property_data.get("bathrooms"),
            surface=property_data.get("surface"),
            surface_unit=property_data.get("surface_unit", "m²"),
            city=property_data.get("city"),
            region=property_data.get("region"),
            property_type=property_data.get("property_type"),
            image_urls=[str(url) for url in property_data.get("image_urls", [])],
        )
        self.db.add(new_property)
        return new_property

    def save_properties_batch(
        self, properties: List[PropertyCreate], base_url: Optional[str] = None
    ) -> None:
        """
        Save a batch of properties to the database

        Args:
            properties: List of PropertyCreate objects to save
            base_url: Optional base URL for checking invalid URLs
        """
        # Collect all URLs for batch processing
        all_urls = [str(prop.url) for prop in properties if prop.url]

        # Get existing property URLs in a single query
        existing_properties = self.check_existing_property_urls(all_urls)

        logger.info(
            f"Found {len(existing_properties)} existing properties out of {len(properties)} scraped"
        )

        # Process properties in batches
        for i, prop_data in enumerate(properties):
            try:
                # Skip properties without valid URLs or that match the base URL only
                if not prop_data.url or (base_url and prop_data.url == f"{base_url}/"):
                    logger.warning(
                        f"Skipping property with invalid URL: {prop_data.url}"
                    )
                    continue

                # Ensure all string fields are truncated to their max lengths
                if prop_data.title and len(prop_data.title) > 256:
                    prop_data.title = prop_data.title[:252] + "..."

                if prop_data.property_type and len(prop_data.property_type) > 128:
                    prop_data.property_type = prop_data.property_type[:124] + "..."

                if prop_data.city and len(prop_data.city) > 128:
                    prop_data.city = prop_data.city[:124] + "..."

                if prop_data.region and len(prop_data.region) > 128:
                    prop_data.region = prop_data.region[:124] + "..."

                if prop_data.surface_unit and len(prop_data.surface_unit) > 10:
                    prop_data.surface_unit = prop_data.surface_unit[:10]

                if str(prop_data.url) in existing_properties:
                    # Update existing property
                    self.update_property(
                        existing_properties[str(prop_data.url)], prop_data.model_dump()
                    )
                    logger.debug(f"Updated existing property: {prop_data.url}")
                else:
                    # Create new property
                    self.create_property(prop_data.model_dump())
                    logger.debug(f"Added new property: {prop_data.url}")

                # Commit in smaller batches to avoid large transactions
                if i > 0 and i % 50 == 0:
                    try:
                        self.db.commit()
                        logger.info(
                            f"Committed batch of properties: {i}/{len(properties)}"
                        )
                    except IntegrityError as e:
                        logger.error(f"Integrity error during batch commit: {str(e)}")
                        self.db.rollback()

            except Exception as e:
                logger.error(f"Error saving property to database: {str(e)}")
                continue

        # Final commit for remaining properties
        try:
            self.db.commit()
            logger.info(f"Successfully saved {len(properties)} properties to database")
        except IntegrityError as e:
            logger.error(f"Integrity error during final commit: {str(e)}")
            self.db.rollback()
