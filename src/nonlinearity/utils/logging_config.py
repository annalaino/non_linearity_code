"""
Logging configuration using loguru.

Provides centralized logging setup for the project.
"""

import sys
from pathlib import Path
from loguru import logger


def setup_logging(
    log_file: Path = None,
    level: str = "INFO",
    format_string: str = None
) -> None:
    """
    Configure loguru for the application.
    
    Args:
        log_file: Optional path to log file.
        level: Log level (DEBUG, INFO, WARNING, ERROR).
        format_string: Custom format string.
    """
    # Remove default handler
    logger.remove()
    
    # Default format
    if format_string is None:
        format_string = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )
    
    # Add console handler
    logger.add(
        sys.stderr,
        format=format_string,
        level=level,
        colorize=True,
    )
    
    # Add file handler if specified
    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        logger.add(
            log_file,
            format=format_string,
            level=level,
            rotation="10 MB",
            retention="7 days",
            compression="zip",
        )
    
    logger.info(f"Logging initialized at {level} level")


def get_logger(name: str = None):
    """
    Get a logger instance.
    
    Args:
        name: Optional name for the logger.
    
    Returns:
        Logger instance.
    """
    if name:
        return logger.bind(name=name)
    return logger


# Default logger instance
log = get_logger()
