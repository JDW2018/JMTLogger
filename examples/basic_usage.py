"""
Basic usage example of the JMTLogger.
"""

from jmtlogger import JMTLogger
import time


def main():
    """Demonstrate basic logger usage."""
    # Create a logger with default settings
    logger = JMTLogger(
        name="basic_example",
        log_to_console=True,
        log_to_file=True,
        log_file="basic_example.log",
        log_level="INFO"
    )
    
    # Log messages at different levels
    logger.debug("This is a debug message")
    logger.info("Application started successfully")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    
    # Log with formatting
    user_name = "Alice"
    user_id = 12345
    logger.info("User %s (ID: %d) logged in", user_name, user_id)
    
    # Log with exception information
    try:
        result = 10 / 0
    except ZeroDivisionError:
        logger.exception("Division by zero error occurred")
    
    # Change log level dynamically
    logger.set_level("DEBUG")
    logger.debug("This debug message will now be visible")
    
    # Check if logging is enabled for a level
    if logger.is_enabled_for("INFO"):
        logger.info("Info logging is enabled")
    
    # Context manager usage
    with JMTLogger(name="context_logger", log_to_console=True) as ctx_logger:
        ctx_logger.info("This logger will be automatically closed")
    
    logger.info("Basic example completed")
    
    # Close the logger
    logger.close()


if __name__ == "__main__":
    main()
