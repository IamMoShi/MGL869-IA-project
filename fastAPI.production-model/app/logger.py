import logging
from logging.handlers import RotatingFileHandler
import os
import datetime

# Create log directory if needed
os.makedirs("/usr/share/logs", exist_ok=True)

# Configure RotatingFileHandler
log_file = "/usr/share/logs/fastAPI.production-model.csv"
handler = RotatingFileHandler(
    log_file,
    maxBytes=1024 * 10,  # 10 KB
    backupCount=10       # Keep 10 rotated logs
)

# Define a formatter with a custom date format
formatter = logging.Formatter(
    fmt='%(asctime)s,%(levelname)s,%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)

# Create the logger
logger = logging.getLogger("fastAPI.production-model")
logger.setLevel(logging.DEBUG)  # Set minimum log level
logger.addHandler(handler)

# Optional: avoid duplicate logs if root logger has handlers
logger.propagate = False

# Define your CSV-style message builder
def makeMessage(errorType, sourceService, apiEndpoint, val1, val2, message, request_ID=''):
    current_time_unix = int(datetime.datetime.utcnow().timestamp() * 1000)
    return f"{current_time_unix},{errorType},{sourceService},{apiEndpoint},{val1},{val2},{message},{request_ID}"

# Example usage