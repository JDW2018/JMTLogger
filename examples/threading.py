"""
Threading usage example of the JMTLogger.
"""

import threading
import time
import queue
from jmtlogger import JMTLogger


def worker_thread(thread_id: int, shared_queue: queue.Queue, logger_name: str):
    """Worker function that runs in a separate thread."""
    # Get the shared logger
    logger = JMTLogger(
        name=logger_name,
        log_to_console=True,
        log_to_file=True,
        log_file="threading_example.log",
        log_level="INFO"
    )
    
    thread_name = threading.current_thread().name
    logger.info(f"Thread {thread_id} ({thread_name}) started")
    
    # Simulate work with shared resources
    try:
        while True:
            try:
                item = shared_queue.get(timeout=1.0)
                if item is None:  # Sentinel value to stop
                    break
                
                logger.info(f"Thread {thread_id} processing item: {item}")
                
                # Simulate processing time
                time.sleep(0.3)
                
                # Simulate occasional errors
                if item % 7 == 0:
                    logger.warning(f"Thread {thread_id} - Item {item} requires special handling")
                
                shared_queue.task_done()
                
            except queue.Empty:
                logger.debug(f"Thread {thread_id} - No items in queue, continuing...")
                break
                
    except Exception as e:
        logger.error(f"Thread {thread_id} encountered an error: {e}")
        logger.exception("Full traceback:")
    
    logger.info(f"Thread {thread_id} ({thread_name}) finished")


def main():
    """Demonstrate threading logger usage."""
    # Set up the main logger
    main_logger = JMTLogger(
        name="threading_main",
        log_to_console=True,
        log_to_file=True,
        log_file="threading_example.log",
        log_level="INFO"
    )
    
    main_logger.info("Starting threading example")
    
    # Create a shared queue and populate it with work items
    work_queue = queue.Queue()
    num_items = 20
    
    main_logger.info(f"Adding {num_items} items to work queue")
    for i in range(num_items):
        work_queue.put(i)
    
    # Create and start multiple threads
    num_threads = 4
    threads = []
    
    main_logger.info(f"Creating {num_threads} worker threads")
    
    for thread_id in range(num_threads):
        thread = threading.Thread(
            target=worker_thread,
            args=(thread_id, work_queue, "threading_worker"),
            name=f"Worker-{thread_id}"
        )
        threads.append(thread)
        thread.start()
        main_logger.info(f"Started thread {thread_id}: {thread.name}")
    
    # Wait for all items to be processed
    main_logger.info("Waiting for all work items to be processed...")
    work_queue.join()
    
    # Signal threads to stop by adding sentinel values
    for _ in range(num_threads):
        work_queue.put(None)
    
    # Wait for all threads to complete
    for i, thread in enumerate(threads):
        thread.join()
        main_logger.info(f"Thread {i} ({thread.name}) joined")
    
    main_logger.info("All worker threads completed")
    main_logger.info("Threading example finished")
    main_logger.close()


if __name__ == "__main__":
    main()
