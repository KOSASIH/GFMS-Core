# src/utils/logger.py

import logging
import os

def setup_logger(name: str, log_file: str, level=logging.INFO):
    """Set up a logger with a specified name and log file."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create file handler
    fh = logging.FileHandler(log_file)
    fh.setLevel(level)
    
    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    
    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    # Add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger

# Example usage
logger = setup_logger('GFMS', os.path.join(os.getcwd(), 'gfms.log'))
