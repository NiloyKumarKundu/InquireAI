import logging
import os
from datetime import datetime

def setup_logging():
    log_dir = "app/logs"
    os.makedirs(log_dir, exist_ok=True)  # Ensure the logs directory exists
    log_file = os.path.join(log_dir, f"app_log_{datetime.now().strftime('%Y%m%d')}.log")

    # Create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Prevent adding multiple handlers if function is called multiple times
    if not logger.handlers:
        # File handler (writes logs to a file)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s %(module)s - %(message)s"))

        # Console handler (prints logs to the console)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    logger.info("Logging setup complete.")  # This log will be saved and printed
    return logger  # Return logger for reuse

# Initialize and get logger
logger = setup_logging()