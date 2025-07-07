"""
Custom handlers for multiprocessing-safe logging.
"""

import logging
import logging.handlers
import multiprocessing
import threading
import queue
import atexit
from typing import Optional, Any
from pathlib import Path


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


def create_console_handler(formatter: logging.Formatter) -> logging.Handler:
    """Create a console handler with the specified formatter."""
    handler = logging.StreamHandler()
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
