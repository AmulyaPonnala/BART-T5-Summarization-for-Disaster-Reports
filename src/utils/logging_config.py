"""
Logging configuration for clear, readable logs
"""

import logging
import sys
from datetime import datetime


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for different log levels"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        # Add color to the level name
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.RESET}"
        
        return super().format(record)


def setup_logging(level=logging.INFO, use_colors=True):
    """
    Setup logging with clear, readable format
    
    Args:
        level: Logging level (default: INFO)
        use_colors: Whether to use colored output (default: True)
    """
    # Create formatter
    if use_colors and sys.stdout.isatty():
        # Use colored formatter if terminal supports it
        formatter = ColoredFormatter(
            fmt='[%(asctime)s] %(levelname)-8s %(message)s',
            datefmt='%H:%M:%S'
        )
    else:
        # Plain formatter
        formatter = logging.Formatter(
            fmt='[%(asctime)s] %(levelname)-8s %(message)s',
            datefmt='%H:%M:%S'
        )
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    root_logger.addHandler(console_handler)
    
    return root_logger

