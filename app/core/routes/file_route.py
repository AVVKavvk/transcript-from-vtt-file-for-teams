from fastapi import Body, Form, HTTPException, APIRouter, File, UploadFile
from typing import Optional
from fastapi.responses import JSONResponse
from app.utils.logger import logger
from app.core.config.setting import LocalSettings
from app.core.handlers.file_handler import FileHandler

router = APIRouter(
    tags=["File"],
    # dependencies=[Depends(verify_token)],
    responses={404: {"description": "Not found"}},
)


@router.post("/upload", summary="Upload VTT transcript and extract tasks automatically")
async def upload_meeting_transcript(
    file: UploadFile = File(..., description="VTT transcript file"),
    meeting_title: str = Form(..., description="Meeting title"),
    meeting_date: Optional[str] = Form(None, description="Meeting date (ISO8601)")
):
    """Upload VTT transcript and extract tasks automatically"""
    try:
        # Validate file type
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file name provided")

        if not file.filename.endswith('.vtt'):
            raise HTTPException(status_code=400, detail="Only .vtt files are supported")

        # Read file content
        content = await file.read()
        vtt_content = content.decode('utf-8')

        # Handle file upload
        file_handler = FileHandler(LocalSettings.DB_NAME)
        result = await file_handler.handle_file_upload(meeting_title, vtt_content, meeting_date)

        return JSONResponse(content=result, status_code=201)
    except Exception as e:
        logger.error(f"Failed to upload meeting transcript: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload meeting transcript")
