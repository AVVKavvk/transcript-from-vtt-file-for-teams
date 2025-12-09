from pydantic import BaseModel, Field
from typing import List, Literal, Optional


class Task(BaseModel):
    """Individual task/action item from meeting"""
    assigneeName: str = Field(description="Full name of person assigned to this task")
    assigneeEmail: Optional[str] = Field(None, description="Email address of assignee if available")
    taskTitle: str = Field(description="Brief title/summary of the task (max 100 chars)")
    taskDescription: str = Field(description="Detailed description with context (2-4 lines)")
    priority: Literal["low", "medium", "high"] = Field(
        description="Priority level: high=urgent/critical/blocking, medium=normal, low=nice-to-have"
    )
    dueDate: Optional[str] = Field(
        None,
        description="Due date in ISO8601 format (YYYY-MM-DDTHH:MM:SSZ) if mentioned"
    )


class MeetingExtraction(BaseModel):
    """Complete extraction result from meeting transcript"""
    summary: str = Field(
        description="Comprehensive 3-5 paragraph summary covering key points, decisions, and next steps"
    )
    tasks: List[Task] = Field(
        default_factory=list,
        description="List of all actionable tasks extracted from the meeting"
    )
