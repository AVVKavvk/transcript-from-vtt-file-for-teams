from fastapi import Body, Form, HTTPException, APIRouter, File, UploadFile
from typing import Optional
from fastapi.responses import JSONResponse
from app.utils.logger import logger
from app.core.config.setting import LocalSettings
from app.core.handlers.task_handler import TaskHandler

router = APIRouter(
    tags=["Task"],
    # dependencies=[Depends(verify_token)],
    responses={404: {"description": "Not found"}},
)


@router.get("/all", summary="Get all tasks")
async def get_all_tasks():
    try:
        task_handler = TaskHandler(LocalSettings.DB_NAME)
        result = await task_handler.get_all_tasks()
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        logger.error(f"Failed to get all tasks: {e}")
        raise HTTPException(status_code=500, detail="Failed to get all tasks")


@router.get("/meeting/{meeting_id}", summary="Get tasks by meeting id")
async def get_tasks_by_meeting_id(meeting_id: str):
    try:
        task_handler = TaskHandler(LocalSettings.DB_NAME)
        result = await task_handler.get_tasks_by_meeting_id(meeting_id)
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        logger.error(f"Failed to get tasks by meeting id: {e}")
        raise HTTPException(status_code=500, detail="Failed to get tasks by meeting id")


@router.get("/{task_id}", summary="Get task by id")
async def get_task_by_id(task_id: str):
    try:
        task_handler = TaskHandler(LocalSettings.DB_NAME)
        result = await task_handler.get_task_by_id(task_id)
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        logger.error(f"Failed to get task by id: {e}")
        raise HTTPException(status_code=500, detail="Failed to get task by id")
