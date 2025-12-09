from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any


class TaskModel(BaseModel):
    meeting_id: str
    task_id: str
    assignee_name: str = Field(..., description="Name of the person assigned")
    assignee_email: Optional[str] = Field(None, description="Email of assignee")
    task_title: str = Field(..., description="Short task summary")
    task_description: str = Field(..., description="Detailed task context")
    priority: str = Field(..., pattern="^(low|medium|high)$")
    due_date: Optional[str] = Field(None, description="ISO8601 due date")
    status: str = Field(default="pending", pattern="^(pending|in_progress|completed|cancelled)$")
    created_at: str = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at: str = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    class Config:
        json_schema_extra = {
            "example": {
                "assignee_name": "Priya",
                "assignee_email": "priya@company.com",
                "task_title": "Prepare API specification",
                "task_description": "Draft detailed API spec for billing integration",
                "priority": "high",
                "due_date": "2025-12-14T00:00:00Z",
                "status": "pending"
            }
        }


class MeetingModel(BaseModel):
    meeting_id: str
    meeting_title: str
    meeting_date: Optional[str] = None
    participants: List[Dict[Any, Any]] = Field(default_factory=List)
    transcript: str
    summary: Optional[str] = None
    task_ids: List[str] = Field(default_factory=list)
    created_at: str = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


class TaskUpdateModel(BaseModel):
    assignee_name: Optional[str] = None
    assignee_email: Optional[str] = None
    task_title: Optional[str] = None
    task_description: Optional[str] = None
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    due_date: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(pending|in_progress|completed|cancelled)$")
