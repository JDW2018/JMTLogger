"""
Custom handlers for multiprocessing-safe logging.
"""

import logging
import logging.handlers
import multiprocessing
import threading
import queue
import atexit
import sys
import os
from typing import Optional, Any, Dict
from pathlib import Path


class ColoredFormatter(logging.Formatter):
    """
    A formatter that adds color codes to log messages based on log level.
    Works on both Windows and Unix-like systems.
    """
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    
    RESET = '\033[0m'
    
    def __init__(self, *args, use_colors: bool = None, **kwargs):
        """
        Initialize the colored formatter.
        
        Args:
            use_colors: Whether to use colors. If None, auto-detect based on terminal support.
        """
        super().__init__(*args, **kwargs)
        
        if use_colors is None:
            # Auto-detect color support
            self.use_colors = self._supports_color()
        else:
            self.use_colors = use_colors
        
        # Enable ANSI color support on Windows 10+
        if self.use_colors and os.name == 'nt':
            self._enable_windows_ansi()
    
    def _supports_color(self) -> bool:
        """
        Check if the terminal supports colors.
        """
        # Check if we're in a terminal
        if not hasattr(sys.stdout, 'isatty') or not sys.stdout.isatty():
            return False
        
        # Check environment variables
        if os.getenv('NO_COLOR'):
            return False
        
        if os.getenv('FORCE_COLOR'):
            return True
        
        # Windows terminal detection
        if os.name == 'nt':
            # Windows 10 version 1511 and later support ANSI escape sequences
            try:
                import platform
                version = platform.version()
                major, minor, build = map(int, version.split('.'))
                return major >= 10 and build >= 10586
            except:
                return False
        
        # Unix-like systems
        term = os.getenv('TERM', '').lower()
        if 'color' in term or term in ['xterm', 'xterm-256color', 'screen', 'linux']:
            return True
        
        return False
    
    def _enable_windows_ansi(self) -> None:
        """
        Enable ANSI escape sequence processing on Windows.
        """
        try:
            import ctypes
            from ctypes import wintypes
            
            kernel32 = ctypes.windll.kernel32
            
            # Get stdout handle
            stdout_handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
            
            # Get current console mode
            mode = wintypes.DWORD()
            kernel32.GetConsoleMode(stdout_handle, ctypes.byref(mode))
            
            # Enable virtual terminal processing (ANSI escape sequences)
            ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
            kernel32.SetConsoleMode(stdout_handle, mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)
        except Exception:
            # If we can't enable ANSI support, disable colors
            self.use_colors = False
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record with colors if enabled.
        """
        if not self.use_colors:
            return super().format(record)
        
        # Get the color for this log level
        level_color = self.COLORS.get(record.levelname, '')
        
        # Format the message normally first
        formatted_message = super().format(record)
        
        # Add color codes around the entire message
        if level_color:
            formatted_message = f"{level_color}{formatted_message}{self.RESET}"
        
        return formatted_message


class MultiprocessingHandler(logging.Handler):
    """
    A handler that safely handles logging from multiple processes.
    
    This handler uses a queue to collect log records from multiple processes
    and a separate thread to write them to the actual handlers.
    """
    
    def __init__(self, handler: logging.Handler) -> None:
        """
        Initialize the multiprocessing handler.
        
        Args:
            handler: The actual handler to write log records to
        """
        super().__init__()
        self._handler = handler
        self._queue: multiprocessing.Queue = multiprocessing.Queue()
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self.start()
        
    def start(self) -> None:
        """Start the logging thread."""
        if self._thread is None or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._worker, daemon=True)
            self._thread.start()
            atexit.register(self.stop)
    
    def stop(self) -> None:
        """Stop the logging thread."""
        if self._thread and self._thread.is_alive():
            self._stop_event.set()
            # Send sentinel to wake up the worker
            try:
                self._queue.put_nowait(None)
            except:
                pass
            self._thread.join(timeout=1.0)
    
    def _worker(self) -> None:
        """Worker thread that processes log records from the queue."""
        while not self._stop_event.is_set():
            try:
                record = self._queue.get(timeout=0.1)
                if record is None:  # Sentinel value to stop
                    break
                self._handler.emit(record)
            except queue.Empty:
                continue
            except Exception:
                # Ignore errors in the worker thread to prevent deadlocks
                pass
    
    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record by putting it in the queue."""
        try:
            # Format exception info if present to make record picklable
            if record.exc_info:
                record.exc_text = self.format(record)
                record.exc_info = None
            record.stack_info = None
            self._queue.put_nowait(record)
        except:
            # If queue is full, drop the record to prevent blocking
            pass
    
    def close(self) -> None:
        """Close the handler and clean up resources."""
        self.stop()
        self._handler.close()
        super().close()


class SafeRotatingFileHandler(logging.handlers.RotatingFileHandler):
    """
    A rotating file handler that's safe for multiprocessing.
    
    This handler uses file locking to ensure that only one process
    can write to the log file at a time.
    """
    
    def __init__(self, filename: Path, mode: str = 'a', maxBytes: int = 0,
                 backupCount: int = 0, encoding: Optional[str] = None,
                 delay: bool = False) -> None:
        """Initialize the safe rotating file handler."""
        super().__init__(str(filename), mode, maxBytes, backupCount, encoding, delay)
        self._lock = multiprocessing.Lock()
    
    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record with file locking."""
        with self._lock:
            super().emit(record)


def create_console_handler(formatter: logging.Formatter, use_colors: bool = True) -> logging.Handler:
    """
    Create a console handler with the specified formatter.
    
    Args:
        formatter: The base formatter to use
        use_colors: Whether to enable colored output (auto-detected if True)
    """
    handler = logging.StreamHandler()
    
    # If colors are requested and we have a regular formatter, wrap it with colors
    if use_colors and not isinstance(formatter, ColoredFormatter):
        # Create a colored formatter with the same format string
        colored_formatter = ColoredFormatter(
            fmt=formatter._fmt,
            datefmt=formatter.datefmt,
            use_colors=True
        )
        handler.setFormatter(colored_formatter)
    else:
        handler.setFormatter(formatter)
    
    return handler


def create_file_handler(
    log_file: Path,
    formatter: logging.Formatter,
    max_file_size: int = 10 * 1024 * 1024,
    backup_count: int = 5
) -> logging.Handler:
    """Create a rotating file handler with the specified formatter."""
    handler = SafeRotatingFileHandler(
        log_file,
        maxBytes=max_file_size,
        backupCount=backup_count,
        encoding='utf-8'
    )
    handler.setFormatter(formatter)
    return handler


def create_multiprocessing_handler(base_handler: logging.Handler) -> MultiprocessingHandler:
    """Create a multiprocessing-safe wrapper around a base handler."""
    return MultiprocessingHandler(base_handler)
