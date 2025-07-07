"""
Example showing how to import and use the jmtlogger in another project.
"""

# Simple import and usage
from jmtlogger import JMTLogger

def main():
    """Example of using jmtlogger in your own project."""
    
    # Create a logger for your application
    app_logger = JMTLogger(
        name="my_application",
        log_to_console=True,
        log_to_file=True,
        log_file="my_app.log",
        log_level="INFO"
    )
    
    # Use it throughout your application
    app_logger.info("Application starting...")
    
    try:
        # Your application logic here
        data = {"users": 100, "active": 85}
        app_logger.info("Current stats: %s", data)
        
        # Simulate processing
        for i in range(3):
            app_logger.debug("Processing step %d", i+1)
        
        app_logger.info("Processing completed successfully")
        
    except Exception as e:
        app_logger.error("An error occurred: %s", e)
        app_logger.exception("Full traceback:")
    
    finally:
        app_logger.info("Application shutting down...")
        app_logger.close()

if __name__ == "__main__":
    main()
