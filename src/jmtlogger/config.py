"""
Configuration management for the multiprocessing logger.
"""

from dataclasses import dataclass
from typing import Optional, Union
from pathlib import Path
import logging


@dataclass
class LoggerConfig:
    """Configuration class for the JMTLogger."""
    
    name: str = "jmt_logger"
    log_level: Union[str, int] = logging.INFO
    log_to_console: bool = True
    log_to_file: bool = False
    log_file: Optional[Union[str, Path]] = None
    log_dir: Optional[Union[str, Path]] = None
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    console_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(processName)s - %(threadName)s - %(message)s"
    file_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(processName)s - %(threadName)s - %(funcName)s:%(lineno)d - %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"
    use_colors: bool = True  # Enable colored console output
    
    def __post_init__(self) -> None:
        """Validate and normalize configuration after initialization."""
        # Convert string log level to integer
        if isinstance(self.log_level, str):
            self.log_level = getattr(logging, self.log_level.upper(), logging.INFO)
        
        # Ensure log file is specified if logging to file
        if self.log_to_file and not self.log_file:
            if self.log_dir:
                self.log_file = Path(self.log_dir) / f"{self.name}.log"
            else:
                self.log_file = f"{self.name}.log"
        
        # Convert log_file to Path object
        if self.log_file:
            self.log_file = Path(self.log_file)
            # Create directory if it doesn't exist
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def from_dict(cls, config_dict: dict) -> "LoggerConfig":
        """Create LoggerConfig from dictionary."""
        return cls(**config_dict)
    
    def to_dict(self) -> dict:
        """Convert LoggerConfig to dictionary."""
        return {
            "name": self.name,
            "log_level": self.log_level,
            "log_to_console": self.log_to_console,
            "log_to_file": self.log_to_file,
            "log_file": str(self.log_file) if self.log_file else None,
            "log_dir": str(self.log_dir) if self.log_dir else None,
            "max_file_size": self.max_file_size,
            "backup_count": self.backup_count,
            "console_format": self.console_format,
            "file_format": self.file_format,
            "date_format": self.date_format,
            "use_colors": self.use_colors,
        }
