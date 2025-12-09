from app.utils.logger import logger
from typing import Any, List
from app.core.config.db import mongo_client
from app.core.config.setting import LocalSettings
from app.core.models.db_model import TaskModel


class TaskService:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.task_collection = mongo_client[self.db_name][LocalSettings.TASK_COLLECTION]

    async def get_all_tasks_service(self) -> List[TaskModel]:
        try:
            result = await self.task_collection.find({}).sort({"_id": -1}).to_list(length=None) or []
            return [TaskModel(**task) for task in result]
        except Exception as e:
            logger.error(f"Failed to get all tasks: {e}")
            raise e

    async def get_task_by_id_service(self, task_id: str) -> TaskModel | None:
        try:
            result = await self.task_collection.find_one({"task_id": task_id})
            if not result:
                return None
            return TaskModel(**result) or None
        except Exception as e:
            logger.error(f"Failed to get task by id: {e}")
            raise e

    async def get_tasks_by_meeting_id_service(self, meeting_id: str) -> List[TaskModel]:
        try:
            result = await self.task_collection.find({"meeting_id": meeting_id}).sort({"_id": -1}).to_list(length=None) or []
            return [TaskModel(**task) for task in result]
        except Exception as e:
            logger.error(f"Failed to get tasks by meeting id: {e}")
            raise e
