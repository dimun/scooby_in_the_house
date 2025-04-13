import logging
import asyncio
import traceback
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional

from app.scrapers.fincaraiz import FincaRaizScraper
from app.db.repositories.task_repository import TaskRepository
from app.db.repositories import PropertyRepository

logger = logging.getLogger(__name__)

# Keep a small in-memory cache of recent logs (for endpoints that need quick access)
SCRAPER_LOGS: List[Dict[str, Any]] = []
MAX_LOG_ENTRIES = 100


async def _run_scraper(
    task_id: str,
    city: str,
    region: str,
    property_type: str,
    max_pages: int,
    db: Session,
) -> None:
    """
    Internal function to run the scraper asynchronously
    """
    task_repo = TaskRepository(db)
    property_repo = PropertyRepository(db)
    total_properties = 0

    try:
        start_time = datetime.now()
        log_message = f"[Task {task_id}] Starting scraping for {property_type} in {city}, {region} at {start_time}"
        logger.info(log_message)
        _add_log_entry(task_id, "info", log_message)

        # Update task status to running
        task_repo.update_task_status(task_id, "running")

        async with FincaRaizScraper() as scraper:
            async for page_listings in scraper.get_property_listings(
                city, region, property_type, max_pages
            ):
                if not page_listings:
                    continue

                total_properties += len(page_listings)
                log_message = f"[Task {task_id}] Found {len(page_listings)} properties on current page. Total so far: {total_properties}"
                logger.info(log_message)
                _add_log_entry(task_id, "info", log_message)
                
                # Update task status with progress
                task_repo.update_task_status(
                    task_id,
                    "running",
                    properties_found=total_properties,
                )

                # Save current page's properties to database
                property_repo.save_properties_batch(page_listings)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        log_message = f"[Task {task_id}] Scraping completed for {property_type} in {city}, {region}. Total properties: {total_properties}. Duration: {duration}s"
        logger.info(log_message)
        _add_log_entry(task_id, "info", log_message)

        # Update task status with results
        task_repo.update_task_status(
            task_id, "completed", properties_found=total_properties
        )

    except Exception as e:
        error_msg = str(e)
        traceback.print_exc()
        log_message = f"[Task {task_id}] Error during scraping: {error_msg}"
        logger.error(log_message)
        _add_log_entry(task_id, "error", log_message)

        # Update task status with error
        task_repo.update_task_status(task_id, "failed", error=error_msg)


async def scrape_properties(
    city: str,
    region: str,
    property_type: str,
    max_pages: int = 5,
    db: Session = None,
    task_id: str = None,
) -> str:
    """
    Run the property scraper and save results to the database
    This function is meant to be run as a background task

    Args:
        city: The city to search in
        region: The region/area within the city
        property_type: Type of properties to search for (e.g., "casas-y-apartamentos", "fincas", "casas-campestres", "cabanas")
                       Multiple types can be combined with "-y-" (e.g., "fincas-y-casas-campestres")
        max_pages: Maximum number of pages to scrape
        db: Database session
        task_id: Optional task ID to use (will generate one if not provided)

    Returns:
        The task ID
    """
    if task_id is None:
        task_id = str(uuid.uuid4())[:8]

    # Create task in database
    task_repo = TaskRepository(db)
    task_repo.create_task(
        {
            "id": task_id,
            "city": city,
            "region": region,
            "property_type": property_type,
            "max_pages": max_pages,
            "status": "pending",
            "start_time": datetime.now(),
        }
    )

    await _run_scraper(task_id, city, region, property_type, max_pages, db)
    return task_id


def _add_log_entry(task_id: str, level: str, message: str) -> None:
    """Add a log entry to the in-memory log cache"""
    timestamp = datetime.now().isoformat()

    SCRAPER_LOGS.append(
        {"task_id": task_id, "level": level, "message": message, "timestamp": timestamp}
    )

    # Keep the log size under control
    if len(SCRAPER_LOGS) > MAX_LOG_ENTRIES:
        SCRAPER_LOGS.pop(0)  # Remove oldest entry


def get_task_logs(
    task_id: Optional[str] = None, limit: int = 50
) -> List[Dict[str, Any]]:
    """
    Get recent scraper logs from memory

    Args:
        task_id: Optional task ID to filter logs
        limit: Maximum number of logs to return

    Returns:
        List of log entries
    """
    if task_id:
        # Filter logs by task_id
        logs = [log for log in SCRAPER_LOGS if log["task_id"] == task_id]
    else:
        logs = SCRAPER_LOGS.copy()

    # Return the most recent logs up to the limit
    return logs[-limit:] if logs else []


def get_task_status(task_id: Optional[str] = None, db: Session = None) -> Any:
    """
    Get task status from database

    Args:
        task_id: The ID of the task to get status for, or None to get all tasks
        db: Database session

    Returns:
        Task or list of tasks
    """
    if not db:
        return None

    task_repo = TaskRepository(db)

    if task_id:
        return task_repo.get_task(task_id)

    return task_repo.get_tasks(limit=20)
