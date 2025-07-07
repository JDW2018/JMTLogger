"""
Test script to demonstrate colored console output.
"""

from jmtlogger import JMTLogger

def main():
    """Test colored console output with different log levels."""
    
    # Create logger with colors enabled (default)
    print("=== Testing Colored Console Output ===")
    logger = JMTLogger(
        name="color_test",
        log_to_console=True,
        log_to_file=False,
        log_level="DEBUG",
        use_colors=True
    )
    
    logger.debug("This is a DEBUG message (should be cyan)")
    logger.info("This is an INFO message (should be green)")
    logger.warning("This is a WARNING message (should be yellow)")
    logger.error("This is an ERROR message (should be red)")
    logger.critical("This is a CRITICAL message (should be magenta)")
    
    logger.close()
    
    print("\n=== Testing without Colors ===")
    # Create logger with colors disabled
    logger_no_color = JMTLogger(
        name="no_color_test",
        log_to_console=True,
        log_to_file=False,
        log_level="DEBUG",
        use_colors=False
    )
    
    logger_no_color.debug("This is a DEBUG message (no colors)")
    logger_no_color.info("This is an INFO message (no colors)")
    logger_no_color.warning("This is a WARNING message (no colors)")
    logger_no_color.error("This is an ERROR message (no colors)")
    logger_no_color.critical("This is a CRITICAL message (no colors)")
    
    logger_no_color.close()
    
    print("\n=== Testing with Exception ===")
    # Test exception logging with colors
    logger_exception = JMTLogger(
        name="exception_test",
        log_to_console=True,
        log_to_file=False,
        use_colors=True
    )
    
    try:
        result = 1 / 0
    except ZeroDivisionError:
        logger_exception.exception("Division by zero error with colored output")
    
    logger_exception.close()


if __name__ == "__main__":
    main()
