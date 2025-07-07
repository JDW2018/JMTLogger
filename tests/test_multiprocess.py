"""
Tests for multiprocessing functionality.
"""

import multiprocessing
import tempfile
import time
import os
from pathlib import Path
from jmtlogger import JMTLogger


def worker_process(worker_id: int, log_file: str, num_messages: int):
    """Worker process that logs messages."""
    logger = JMTLogger(
        name=f"worker_{worker_id}",
        log_to_file=True,
        log_file=log_file,
        log_to_console=False,
        log_level="INFO"
    )
    
    for i in range(num_messages):
        logger.info(f"Worker {worker_id} - Message {i+1}")
        time.sleep(0.01)  # Small delay to test concurrency
    
    logger.close()
    return f"Worker {worker_id} completed"


def test_multiprocessing_logging():
    """Test that multiple processes can log safely to the same file."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".log") as temp_file:
        temp_path = temp_file.name
    
    try:
        num_processes = 3
        messages_per_process = 5
        processes = []
        
        # Start multiple processes
        for worker_id in range(num_processes):
            process = multiprocessing.Process(
                target=worker_process,
                args=(worker_id, temp_path, messages_per_process)
            )
            processes.append(process)
            process.start()
        
        # Wait for all processes to complete
        for process in processes:
            process.join()
        
        # Verify that all messages were logged
        assert os.path.exists(temp_path)
        with open(temp_path, 'r') as f:
            content = f.read()
            
        # Check that content is not empty and contains worker messages
        assert len(content.strip()) > 0
        assert "Worker 0 -" in content
        assert "Worker 1 -" in content
        assert "Worker 2 -" in content
        
        # Count total messages (should be at least num_processes * messages_per_process)
        total_lines = len([line for line in content.split('\n') if line.strip()])
        expected_min_messages = num_processes * messages_per_process
        assert total_lines >= expected_min_messages
    
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    test_multiprocessing_logging()
    print("Multiprocessing test passed!")
