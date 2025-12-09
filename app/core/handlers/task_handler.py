from app.utils.logger import logger
from app.core.services.task_service import TaskService
from typing import List, Dict, Any


class TaskHandler:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.task_service = TaskService(self.db_name)

    async def get_all_tasks(self) -> List[Dict[Any, Any]]:
        try:
            result = await self.task_service.get_all_tasks_service()
            return [task.model_dump() for task in result]
        except Exception as e:
            logger.error(f"Failed to get all tasks: {e}")
            raise e

    async def get_tasks_by_meeting_id(self, meeting_id: str) -> List[Dict[Any, Any]]:
        try:
            result = await self.task_service.get_tasks_by_meeting_id_service(meeting_id)
            return [task.model_dump() for task in result]
        except Exception as e:
            logger.error(f"Failed to get tasks by meeting id: {e}")
            raise e

    async def get_task_by_id(self, task_id: str) -> Dict[Any, Any] | None:
        try:
            result = await self.task_service.get_task_by_id_service(task_id)
            return result.model_dump() if result else None
        except Exception as e:
            logger.error(f"Failed to get task by id: {e}")
            raise e
