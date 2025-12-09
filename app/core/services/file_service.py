from typing import Any, Optional, Dict
from app.utils.logger import logger
from app.core.helper.vtt_helper import parse_vtt_file
from app.core.llm.deepseek import extract_tasks_with_deepseek
from datetime import datetime
from app.core.config.db import mongo_client
from app.core.config.setting import LocalSettings
from app.core.models.db_model import TaskModel, MeetingModel
import uuid


class FileService:

    def __init__(self, db_name: str):
        self.db_name = db_name
        self.task_collection = mongo_client[self.db_name][LocalSettings.TASK_COLLECTION]
        self.meeting_collection = mongo_client[self.db_name][LocalSettings.MEETING_COLLECTION]

    async def handle_file_upload_service(self, meeting_title: str, vtt_content: str, meeting_date: Optional[str] = None) -> Dict[Any, Any]:
        try:
            # Parse VTT
            logger.info({
                "message": "Parsing VTT",
            })

            transcript, participants = parse_vtt_file(vtt_content)
            logger.info({
                "message": "Printing transcript",
                "transcript": transcript
            })
            logger.info({
                "message": "Printing participants",
                "participants": participants
            })

            # Parse meeting date
            parsed_date = None
            if meeting_date:
                try:
                    parsed_date = datetime.fromisoformat(meeting_date.replace('Z', '+00:00')).strftime("%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    logger.error(f"Failed to parse meeting date: {e}")
                    parsed_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                parsed_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Extract tasks using DeepSeek
            logger.info({
                "message": "Extracting tasks using DeepSeek",
            })

            extraction_result = await extract_tasks_with_deepseek(
                meeting_title,
                parsed_date,
                participants,
                transcript
            )

            # Save tasks to database
            logger.info({
                "message": "Saving tasks to database",
            })

            task_ids = []
            meeting_id = str(uuid.uuid4())

            for task_data in extraction_result.tasks or []:
                task_id = str(uuid.uuid4())
                task: TaskModel = TaskModel(
                    meeting_id=meeting_id,
                    task_id=task_id,
                    assignee_name=task_data.assigneeName,
                    assignee_email=task_data.assigneeEmail,
                    task_title=task_data.taskTitle,
                    task_description=task_data.taskDescription,
                    priority=task_data.priority or "medium",
                    due_date=task_data.dueDate,
                    status="pending",
                    created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )

                await self.task_collection.insert_one(task.model_dump())
                task_ids.append(task_id)

            # Save meeting to database
            meeting: MeetingModel = MeetingModel(
                meeting_id=meeting_id,
                meeting_title=meeting_title,
                meeting_date=parsed_date,
                participants=participants,
                transcript=transcript,
                summary=extraction_result.summary,
                task_ids=task_ids,
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

            await self.meeting_collection.insert_one(meeting.model_dump())

            return {
                "message": "Meeting transcript processed successfully",
                "meeting_id": meeting_id,
                "tasks_extracted": len(task_ids),
                "task_ids": task_ids,
                "summary": extraction_result.summary
            }
        except Exception as e:
            logger.error({
                "message": "Failed to upload file",
                "error": str(e)
            })
            raise e
