from loguru import logger
import sys, os, json

def setup_logging():
    logger.remove()
    # JSON logs for cloud
    logger.add(sys.stdout, level=os.getenv("LOG_LEVEL", "INFO"),
               serialize=True, backtrace=False, diagnose=False)
