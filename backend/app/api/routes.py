import asyncio
from fastapi import APIRouter, HTTPException, Query, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import get_db
from app.schemas.property import PropertyResponse, ScraperRequest
from app.schemas.task import TaskListResponse, ScrapingLogResponse
from app.core.usecases import PropertyUseCases, ScraperUseCases
from app.services.scraper_service import get_task_status, get_task_logs

router = APIRouter(prefix="/api/v1", tags=["properties"])

@router.get("/properties", response_model=List[PropertyResponse])
async def get_properties(
    city: Optional[str] = Query(None, description="Filter by city"),
    region: Optional[str] = Query(None, description="Filter by region"),
    property_type: Optional[str] = Query(None, description="Filter by property type"),
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    min_rooms: Optional[int] = Query(None, description="Minimum number of rooms"),
    min_bathrooms: Optional[int] = Query(None, description="Minimum number of bathrooms"),
    skip: int = Query(0, description="Skip first N results"),
    limit: int = Query(20, description="Limit to N results"),
    db: Session = Depends(get_db)
):
    """
    Get properties with optional filtering
    """
    property_usecase = PropertyUseCases(db)
    properties = property_usecase.get_properties(
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
    
    return properties

import asyncio

@router.post("/scrape", status_code=202)
async def start_scraper(
    request: ScraperRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Start a scraping job for properties in the given city and region
    """
    if not request.city or not request.region:
        raise HTTPException(status_code=400, detail="City and region are required")
    
    if not request.property_types:
        raise HTTPException(status_code=400, detail="At least one property type is required")
    
    scraper_usecase = ScraperUseCases(db)

    def run_scraper_sync():
        asyncio.run(scraper_usecase.start_scraper(
            city=request.city,
            region=request.region,
            property_types=request.property_types,
            max_pages=request.max_pages or 5
        ))

    # Añadir la tarea de fondo de manera segura
    background_tasks.add_task(run_scraper_sync)

    return {"message": f"Scraping job started for {request.property_types} in {request.city}, {request.region}"}

@router.get("/properties/stats")
async def get_property_stats(db: Session = Depends(get_db)):
    """
    Get statistics about properties in the database
    """
    property_usecase = PropertyUseCases(db)
    return property_usecase.get_property_stats()

@router.get("/scrape/logs", response_model=ScrapingLogResponse)
async def get_scrape_logs(task_id: Optional[str] = None, limit: int = Query(10, ge=1, le=100)):
    """
    Get the most recent scraping logs
    """
    logs = get_task_logs(task_id, limit)
    log_messages = [f"[{log['timestamp']}] {log['level'].upper()}: {log['message']}" for log in logs]
    
    if not log_messages:
        log_messages = ["No recent scraping logs found. Either no tasks have run or they're not being captured in memory."]
        
    return {"logs": log_messages}

@router.get("/scrape/status", response_model=TaskListResponse)
async def check_scrape_status(
    task_id: Optional[str] = None,
    skip: int = Query(0, description="Skip first N results"),
    limit: int = Query(20, description="Limit to N results"),
    db: Session = Depends(get_db)
):
    """
    Get the status of scraping tasks
    """
    from app.db.repositories.task_repository import TaskRepository
    
    task_repo = TaskRepository(db)
    
    if task_id:
        task = get_task_status(task_id, db)
        if not task:
            raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
        tasks = [task]
        total = 1
    else:
        tasks = task_repo.get_tasks(skip=skip, limit=limit)
        total = task_repo.get_task_count()
    
    return {"tasks": tasks, "total": total} 