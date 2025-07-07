"""
Tests for the core JMTLogger functionality.
"""

import logging
import tempfile
import os
from pathlib import Path
from jmtlogger import JMTLogger, LoggerConfig


class TestLoggerConfig:
    """Test the LoggerConfig class."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = LoggerConfig()
        assert config.name == "jmt_logger"
        assert config.log_level == logging.INFO
        assert config.log_to_console is True
        assert config.log_to_file is False
        assert config.log_file is None
    
    def test_config_from_dict(self):
        """Test creating config from dictionary."""
        config_dict = {
            "name": "test_logger",
            "log_level": "DEBUG",
            "log_to_file": True,
            "log_file": "test.log"
        }
        config = LoggerConfig.from_dict(config_dict)
        assert config.name == "test_logger"
        assert config.log_level == logging.DEBUG
        assert config.log_to_file is True
        assert config.log_file == Path("test.log")
    
    def test_config_post_init(self):
        """Test post-initialization processing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LoggerConfig(
                name="test",
                log_to_file=True,
                log_dir=temp_dir
            )
            expected_path = Path(temp_dir) / "test.log"
            assert config.log_file == expected_path


class TestJMTLogger:
    """Test the JMTLogger class."""
    
    def test_logger_creation(self):
        """Test basic logger creation."""
        logger = JMTLogger(name="test_logger")
        assert logger.name == "test_logger"
        assert isinstance(logger.config, LoggerConfig)
        logger.close()
    
    def test_console_logging(self):
        """Test console logging functionality."""
        logger = JMTLogger(
            name="console_test",
            log_to_console=True,
            log_to_file=False,
            log_level="DEBUG"
        )
        
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")
        
        logger.close()
    
    def test_file_logging(self):
        """Test file logging functionality."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".log") as temp_file:
            temp_path = temp_file.name
        
        try:
            logger = JMTLogger(
                name="file_test",
                log_to_console=False,
                log_to_file=True,
                log_file=temp_path,
                log_level="INFO"
            )
            
            logger.info("Test message")
            logger.warning("Test warning")
            logger.close()
            
            # Check if file was created and contains messages
            assert os.path.exists(temp_path)
            with open(temp_path, 'r') as f:
                content = f.read()
                assert "Test message" in content
                assert "Test warning" in content
        
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_log_levels(self):
        """Test different log levels."""
        logger = JMTLogger(name="level_test", log_level="WARNING")
        
        assert logger.get_level() == logging.WARNING
        assert logger.is_enabled_for("WARNING")
        assert logger.is_enabled_for("ERROR")
        assert not logger.is_enabled_for("INFO")
        assert not logger.is_enabled_for("DEBUG")
        
        logger.set_level("DEBUG")
        assert logger.get_level() == logging.DEBUG
        assert logger.is_enabled_for("DEBUG")
        
        logger.close()
    
    def test_context_manager(self):
        """Test logger as context manager."""
        with JMTLogger(name="context_test") as logger:
            assert isinstance(logger, JMTLogger)
            logger.info("Context manager test")
    
    def test_exception_logging(self):
        """Test exception logging with traceback."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".log") as temp_file:
            temp_path = temp_file.name
        
        try:
            logger = JMTLogger(
                name="exception_test",
                log_to_file=True,
                log_file=temp_path,
                log_to_console=False
            )
            
            try:
                raise ValueError("Test exception")
            except ValueError:
                logger.exception("An exception occurred")
            
            logger.close()
            
            # Check if traceback was logged
            with open(temp_path, 'r') as f:
                content = f.read()
                assert "An exception occurred" in content
                assert "ValueError: Test exception" in content
                assert "Traceback" in content
        
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
