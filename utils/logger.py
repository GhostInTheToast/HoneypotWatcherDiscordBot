"""
Logging utility for the Discord bot.
"""
import os

from loguru import logger

from config import config


def setup_logger():
    """Set up the logger with proper configuration."""
    # Remove default logger
    logger.remove()
    
    # Add console logging
    logger.add(
        sink=lambda msg: print(msg, end=""),
        level=config.LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True
    )
    
    # Add file logging
    os.makedirs(os.path.dirname(config.LOG_FILE), exist_ok=True)
    logger.add(
        sink=config.LOG_FILE,
        level=config.LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="10 MB",
        retention="7 days",
        compression="zip"
    )
    
    return logger


# Initialize logger
setup_logger()
