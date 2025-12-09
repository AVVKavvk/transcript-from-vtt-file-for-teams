from fastapi import Body, Form, HTTPException, APIRouter, File, UploadFile
from typing import Optional
from fastapi.responses import JSONResponse
from app.utils.logger import logger
from app.core.config.setting import LocalSettings
from app.core.handlers.meeting_handler import MeetingHandler

router = APIRouter(
    tags=["Meeting"],
    # dependencies=[Depends(verify_token)],
    responses={404: {"description": "Not found"}},
)


@router.get("/all", summary="Get all meetings")
async def get_all_meetings():
    try:
        meeting_handler = MeetingHandler(LocalSettings.DB_NAME)
        result = await meeting_handler.get_all_meetings()
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        logger.error(f"Failed to get all meetings: {e}")
        raise HTTPException(status_code=500, detail="Failed to get all meetings")


@router.get("/{meeting_id}", summary="Get meeting by id")
async def get_meeting_by_id(meeting_id: str):
    try:
        meeting_handler = MeetingHandler(LocalSettings.DB_NAME)
        result = await meeting_handler.get_meeting_by_id(meeting_id)
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        logger.error(f"Failed to get meeting by id: {e}")
        raise HTTPException(status_code=500, detail="Failed to get meeting by id")
