import logging
import sys
from rich.logging import RichHandler

def get_logger(name=None, debug=False):
    """
    Create and configure a logger instance.
    
    Args:
        name: Name for the logger (defaults to root logger if None)
        debug: If True, set log level to DEBUG, otherwise INFO
    
    Returns:
        Configured logger instance
    """
    log_level = logging.DEBUG if debug else logging.INFO
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Remove existing handlers if any
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create console handler with rich formatting
    console_handler = RichHandler(rich_tracebacks=True, show_time=True)
    console_handler.setLevel(log_level)
    
    # Set format
    formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger   