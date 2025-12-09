import os
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi.openapi.docs import get_swagger_ui_html
from app.core.load_all_env import load_all_env

# Routes Import
from app.core.routes.file_route import router as file_v1_router
# from app.core.routes.query_route import router as query_v1_router

app = FastAPI(title="Meeting Transcript Task Extractor", version="1.3", docs_url=None, redoc_url=None)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore

# CORS middleware
CLIENTS = os.getenv("CLIENTS", "").split(",")
CLIENTS = [url.strip() for url in CLIENTS if url.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=CLIENTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
load_all_env()


security = HTTPBasic()
docs_username = os.getenv("DOCS_USERNAME")
docs_password = os.getenv("DOCS_PASSWORD")


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != docs_username or credentials.password != docs_password:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return credentials


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(credentials: HTTPBasicCredentials = Depends(authenticate)):
    # Use fastapi_app instead of app to access openapi_url
    return get_swagger_ui_html(openapi_url=str(app.openapi_url), title="docs")


app.include_router(file_v1_router, prefix="/api/v1/file")
# app.include_router(query_v1_router, prefix="/api/v1/query")


@app.get("/")
def index():
    return {
    "message": "Meeting Transcript Task Extractor API",
    "version": "1.0.0",
    "endpoints": {
        "upload": "POST /api/meetings/upload",
        "get_meetings": "GET /api/meetings",
        "get_tasks": "GET /api/tasks",
    }
}
