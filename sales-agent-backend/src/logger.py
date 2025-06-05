import os
import sys
from datetime import datetime
from loguru import logger
from config import APP_ROOT_PATH

logger.remove()

logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | <level>{level}</level>\n<level>{message}</level>"
)

logger.add(
    os.path.join(APP_ROOT_PATH, "logs", f"log_{datetime.now().strftime('%Y%m%d')}.log")
)