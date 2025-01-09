# src/logging_config.py

import logging
import os

def setup_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("gfms.log"),
            logging.StreamHandler()
        ]
    )
    logging.info("Logging is set up.")

# Call the setup_logging function to configure logging when the module is imported
setup_logging()
