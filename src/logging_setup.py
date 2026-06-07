"""
Logging configuration module for consistent logging across the project.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


def setup_logging(
    logger_name: str,
    log_level: str = "INFO",
    log_to_file: bool = True,
    log_to_console: bool = True
) -> logging.Logger:
    """
    Configure a logger with both file and console handlers.
    
    Args:
        logger_name: Name of the logger (typically __name__)
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Whether to write to file
        log_to_console: Whether to print to console
        
    Returns:
        Configured logger instance
        
    Example:
        logger = setup_logging(__name__)
        logger.info("Processing started")
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Console handler
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper()))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_to_file:
        try:
            from src.config import LOG_DIR  # Import here to avoid circular import
            
            log_dir = Path(LOG_DIR)
            log_dir.mkdir(exist_ok=True, parents=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = log_dir / f"{logger_name.replace('.', '_')}_{timestamp}.log"
            
            file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
            file_handler.setLevel(getattr(logging, log_level.upper()))
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            # اگر log file نتونست ساخت بشه، فقط console logging کن
            print(f"Warning: Could not set up file logging: {e}")
    
    return logger