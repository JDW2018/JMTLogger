"""
Core multiprocessing logger implementation.
"""

import logging
import multiprocessing
import threading
from typing import Optional, Union, Dict, Any
from pathlib import Path

from .config import LoggerConfig
from .handlers import (
    create_console_handler,
    create_file_handler,
    create_multiprocessing_handler,
    ColoredFormatter,
)


class JMTLogger:
    """
    A multiprocessing-safe logger that can handle logging from multiple
    processes and threads simultaneously.
    """
    
    def __init__(
        self,
        name: str = "jmt_logger",
        config: Optional[LoggerConfig] = None,
        **kwargs
    ) -> None:
        """
        Initialize the JMTLogger.
        
        Args:
            name: Logger name
            config: LoggerConfig instance or None to create from kwargs
            **kwargs: Configuration parameters if config is None
        """
        self.name = name
        
        # Create configuration
        if config is None:
            config_dict = {"name": name, **kwargs}
            self.config = LoggerConfig.from_dict(config_dict)
        else:
            self.config = config
        
        # Create the actual logger
        self._logger = logging.getLogger(self.name)
        self._logger.setLevel(self.config.log_level)
        
        # Clear any existing handlers to prevent duplication
        self._logger.handlers.clear()
        
        # Set up handlers
        self._setup_handlers()
        
        # Prevent propagation to root logger
        self._logger.propagate = False
    
    def _setup_handlers(self) -> None:
        """Set up console and/or file handlers based on configuration."""
        # Create formatters
        console_formatter = logging.Formatter(
            self.config.console_format,
            datefmt=self.config.date_format
        )
        file_formatter = logging.Formatter(
            self.config.file_format,
            datefmt=self.config.date_format
        )
        
        # Add console handler if requested
        if self.config.log_to_console:
            console_handler = create_console_handler(console_formatter, self.config.use_colors)
            mp_console_handler = create_multiprocessing_handler(console_handler)
            mp_console_handler.setLevel(self.config.log_level)
            self._logger.addHandler(mp_console_handler)
        
        # Add file handler if requested
        if self.config.log_to_file and self.config.log_file:
            file_handler = create_file_handler(
                self.config.log_file,
                file_formatter,
                self.config.max_file_size,
                self.config.backup_count
            )
            mp_file_handler = create_multiprocessing_handler(file_handler)
            mp_file_handler.setLevel(self.config.log_level)
            self._logger.addHandler(mp_file_handler)
    
    def debug(self, message: str, *args, **kwargs) -> None:
        """Log a debug message."""
        self._logger.debug(message, *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs) -> None:
        """Log an info message."""
        self._logger.info(message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs) -> None:
        """Log a warning message."""
        self._logger.warning(message, *args, **kwargs)
    
    def warn(self, message: str, *args, **kwargs) -> None:
        """Log a warning message (alias for warning)."""
        self.warning(message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs) -> None:
        """Log an error message."""
        self._logger.error(message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs) -> None:
        """Log a critical message."""
        self._logger.critical(message, *args, **kwargs)
    
    def fatal(self, message: str, *args, **kwargs) -> None:
        """Log a fatal message (alias for critical)."""
        self.critical(message, *args, **kwargs)
    
    def exception(self, message: str, *args, **kwargs) -> None:
        """Log an exception message with traceback."""
        self._logger.exception(message, *args, **kwargs)
    
    def log(self, level: Union[int, str], message: str, *args, **kwargs) -> None:
        """Log a message at the specified level."""
        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.INFO)
        self._logger.log(level, message, *args, **kwargs)
    
    def set_level(self, level: Union[int, str]) -> None:
        """Set the logging level."""
        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.INFO)
        self._logger.setLevel(level)
        # Also update config
        self.config.log_level = level
    
    def get_level(self) -> int:
        """Get the current logging level."""
        return self._logger.level
    
    def is_enabled_for(self, level: Union[int, str]) -> bool:
        """Check if logging is enabled for the specified level."""
        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.INFO)
        return self._logger.isEnabledFor(level)
    
    def close(self) -> None:
        """Close all handlers and clean up resources."""
        for handler in self._logger.handlers[:]:
            handler.close()
            self._logger.removeHandler(handler)
    
    def __enter__(self) -> "JMTLogger":
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.close()
    
    def __repr__(self) -> str:
        """String representation of the logger."""
        return f"JMTLogger(name='{self.name}', level={self.get_level()})"
