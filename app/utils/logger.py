import logging
import sys

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

# Avoid adding multiple handlers on reload
if not logger.hasHandlers():
    logger.addHandler(console_handler)