from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from app.models.task import Task

logger = logging.getLogger(__name__)


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID"""
        return self.db.query(Task).filter(Task.id == task_id).first()
    
    def get_tasks(self, skip: int = 0, limit: int = 20) -> List[Task]:
        """Get all tasks with pagination"""
        return self.db.query(Task).order_by(Task.start_time.desc()).offset(skip).limit(limit).all()
    
    def get_task_count(self) -> int:
        """Get total count of tasks"""
        return self.db.query(Task).count()
    
    def get_recent_tasks(self, limit: int = 5) -> List[Task]:
        """Get most recent tasks"""
        return self.db.query(Task).order_by(Task.start_time.desc()).limit(limit).all()
    
    def create_task(self, task_data: Dict[str, Any]) -> Task:
        """Create a new task"""
        new_task = Task(
            id=task_data.get('id'),
            city=task_data.get('city'),
            region=task_data.get('region'),
            property_type=task_data.get('property_type'),
            max_pages=task_data.get('max_pages'),
            status=task_data.get('status', 'pending'),
            start_time=task_data.get('start_time')
        )
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return new_task
    
    def update_task(self, task_id: str, update_data: Dict[str, Any]) -> Optional[Task]:
        """Update a task with new data"""
        task = self.get_task(task_id)
        if not task:
            return None
            
        for key, value in update_data.items():
            if hasattr(task, key):
                setattr(task, key, value)
                
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def update_task_status(self, task_id: str, status: str, properties_found: int = None, 
                          error: str = None) -> Optional[Task]:
        """Update task status and related fields"""
        update_data = {"status": status}
        
        if status == "completed":
            update_data["end_time"] = datetime.now()
            if properties_found is not None:
                update_data["properties_found"] = properties_found
                
            if task := self.get_task(task_id):
                # Calculate duration
                if task.start_time and update_data["end_time"]:
                    duration = (update_data["end_time"] - task.start_time).total_seconds()
                    update_data["duration_seconds"] = int(duration)
        
        elif status == "failed" and error:
            update_data["end_time"] = datetime.now()
            update_data["error"] = error
            
            if task := self.get_task(task_id):
                # Calculate duration for failed tasks too
                if task.start_time and update_data["end_time"]:
                    duration = (update_data["end_time"] - task.start_time).total_seconds()
                    update_data["duration_seconds"] = int(duration)
                    
        return self.update_task(task_id, update_data)
    
    def delete_task(self, task_id: str) -> bool:
        """Delete a task"""
        task = self.get_task(task_id)
        if not task:
            return False
            
        self.db.delete(task)
        self.db.commit()
        return True 