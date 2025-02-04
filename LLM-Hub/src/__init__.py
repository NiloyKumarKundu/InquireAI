import logging
import os
from datetime import datetime

def setup_logging():
    log_dir = "logs/"
    os.makedirs(log_dir, exist_ok=True)  # Ensure the logs directory exists
    log_file = os.path.join(log_dir, f"app_log_{datetime.now().strftime('%Y%m%d')}.log")
    
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logging.info("Logging setup complete.")

logger = logging.getLogger(__name__)