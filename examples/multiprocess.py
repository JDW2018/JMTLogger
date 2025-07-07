"""
Multiprocessing usage example of the JMTLogger.
"""

import multiprocessing
import time
import os
from jmtlogger import JMTLogger


def worker_function(worker_id: int, shared_logger_name: str):
    """Worker function that runs in a separate process."""
    # Create logger in worker process
    logger = JMTLogger(
        name=shared_logger_name,
        log_to_console=True,
        log_to_file=True,
        log_file=f"multiprocess_example.log",
        log_level="INFO"
    )
    
    process_id = os.getpid()
    logger.info(f"Worker {worker_id} started in process {process_id}")
    
    # Simulate some work with logging
    for i in range(5):
        logger.info(f"Worker {worker_id} - Processing item {i+1}")
        time.sleep(0.5)
        
        if i == 2:  # Simulate a warning
            logger.warning(f"Worker {worker_id} - Item {i+1} required special handling")
    
    logger.info(f"Worker {worker_id} completed all tasks")
    logger.close()


def main():
    """Demonstrate multiprocessing logger usage."""
    # Set up the main logger
    main_logger = JMTLogger(
        name="multiprocess_main",
        log_to_console=True,
        log_to_file=True,
        log_file="multiprocess_example.log",
        log_level="INFO"
    )
    
    main_logger.info("Starting multiprocessing example")
    main_logger.info(f"Main process PID: {os.getpid()}")
    
    # Create multiple processes
    num_workers = 3
    processes = []
    
    main_logger.info(f"Creating {num_workers} worker processes")
    
    for worker_id in range(num_workers):
        process = multiprocessing.Process(
            target=worker_function,
            args=(worker_id, "multiprocess_worker")
        )
        processes.append(process)
        process.start()
        main_logger.info(f"Started worker {worker_id} with PID: {process.pid}")
    
    # Wait for all processes to complete
    for i, process in enumerate(processes):
        process.join()
        main_logger.info(f"Worker {i} (PID: {process.pid}) finished")
    
    main_logger.info("All worker processes completed")
    main_logger.info("Multiprocessing example finished")
    main_logger.close()


if __name__ == "__main__":
    # Required for Windows multiprocessing
    multiprocessing.freeze_support()
    main()
