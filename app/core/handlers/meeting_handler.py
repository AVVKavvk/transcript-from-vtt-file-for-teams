from app.utils.logger import logger
from app.core.services.meeting_service import MeetingService
from typing import Dict, Any, List


class MeetingHandler:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.meeting_service = MeetingService(self.db_name)

    async def get_all_meetings(self) -> List[Dict[Any, Any]]:
        try:
            result = await self.meeting_service.get_all_meetings_service()
            return [meeting.model_dump() for meeting in result] or []
        except Exception as e:
            logger.error(f"Failed to get all meetings: {e}")
            raise e

    async def get_meeting_by_id(self, meeting_id: str) -> Dict[Any, Any] | None:
        try:
            result = await self.meeting_service.get_meeting_by_id_service(meeting_id)
            return result.model_dump() if result else None
        except Exception as e:
            logger.error(f"Failed to get meeting by id: {e}")
            raise e
