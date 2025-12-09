import logging
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()


class LocalSettings:
    """
    A class that contains constants for various settings used in the project.
    """
    # Get the project root directory
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    TEMP_DIR = "temp"

    # ENV

    MONGODB_URL = os.getenv("MONGODB_URL")
    DB_NAME = os.getenv("DB_NAME", "MEETING_TASK_EXTRACTION")
    TASK_COLLECTION = "Tasks"
    MEETING_COLLECTION = "Meetings"

    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

    REPLAICE_X_TOKEN = os.getenv("REPLAICE_X_TOKEN")

    DOCS_USERNAME = os.getenv("DOCS_USERNAME")
    DOCS_PASSWORD = os.getenv("DOCS_PASSWORD")

    # Client
    CLIENTS = os.getenv("CLIENTS")
