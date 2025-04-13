from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from app.services.scraper_service import scrape_properties

class ScraperUseCases:
    def __init__(self, db: Session):
        self.db = db
        
    async def start_scraper(
        self,
        city: str,
        region: str,
        property_types: List[str],
        max_pages: int
    ):
        """
        Prepare and start a scraping job
        """
        # Generate a task ID
        task_id = str(uuid.uuid4())[:8]
        
        # Convert list of property types to FincaRaiz format (joined with "-y-")
        fincaraiz_property_type = "-y-".join(property_types)
        
        # Start the scraping process
        task_id = await scrape_properties(
            city=city,
            region=region,
            property_type=fincaraiz_property_type,
            max_pages=max_pages,
            db=self.db,
            task_id=task_id
        )
        
        return {
            "task_id": task_id,
            "message": f"Scraping job started for {fincaraiz_property_type} in {city}, {region}"
        } 