from typing import Optional, Dict, Any
from app.utils.logger import logger
from app.core.services.file_service import FileService


class FileHandler:
    def __init__(self, db_name: str):
        self.db_name = db_name

    async def handle_file_upload(self, meeting_tile: str, vtt_content: str, meeting_date: Optional[str] = None) -> Dict[Any, Any]:
        try:
            result = await FileService(self.db_name).handle_file_upload_service(meeting_tile, vtt_content, meeting_date)
            return result
        except Exception as e:
            logger.error(f"Failed to handle file upload: {e}")
            raise e
