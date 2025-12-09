from app.utils.logger import logger
from typing import List
from app.core.config.db import mongo_client
from app.core.config.setting import LocalSettings
from app.core.models.db_model import MeetingModel


class MeetingService:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.meeting_collection = mongo_client[self.db_name][LocalSettings.MEETING_COLLECTION]

    async def get_all_meetings_service(self) -> List[MeetingModel]:
        try:

            result = await self.meeting_collection.find({}).sort({"_id": -1}).to_list(length=None) or []
            return [MeetingModel(**meeting) for meeting in result]
        except Exception as e:
            logger.error(f"Failed to get all meetings: {e}")
            raise e

    async def get_meeting_by_id_service(self, meeting_id: str) -> MeetingModel | None:
        try:
            result = await self.meeting_collection.find_one({"meeting_id": meeting_id})
            if result is None:
                return None
            return MeetingModel(**result) if result else None
        except Exception as e:
            logger.error(f"Failed to get meeting by id: {e}")
            raise e
