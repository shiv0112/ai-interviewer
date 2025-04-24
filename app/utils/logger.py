import logging
import sys
import os

# Logger configuration
logger = logging.getLogger("ai_interviewer")
logger.setLevel(logging.DEBUG)  # Change to INFO in production

# Formatter
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# File handler
log_file_path = os.path.join("data", "logs", "ai_interviewer.log")  # Path to log file
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)  # Ensure the log directory exists
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.DEBUG)  # Change to INFO or ERROR in production
file_handler.setFormatter(formatter)

# Avoid adding multiple handlers on reload
if not logger.hasHandlers():
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

