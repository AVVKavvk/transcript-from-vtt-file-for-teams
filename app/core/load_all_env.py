from app.utils.logger import logger
import os


def load_all_env():
    required_vars = [
        "MONGODB_URL",
        "DB_NAME",
        "DEEPSEEK_API_KEY",
        "DEEPSEEK_BASE_URL",
        "DOCS_USERNAME",
        "DOCS_PASSWORD",
        "REPLAICE_X_TOKEN",
        "ENV",
        "CLIENTS"
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        raise Exception(f"Missing required environment variables: {', '.join(missing_vars)}")
