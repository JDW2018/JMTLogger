"""
JMTLogger - Multiprocessing Logger Engine

A robust, thread-safe and process-safe logging engine for Python applications.
"""

from .core import JMTLogger
from .config import LoggerConfig

__version__ = "1.0.0"
__all__ = ["JMTLogger", "LoggerConfig"]
