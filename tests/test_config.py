"""
Tests for configuration functionality.
"""

import tempfile
import json
from pathlib import Path
from jmtlogger import LoggerConfig


def test_config_serialization():
    """Test configuration serialization to/from dictionary."""
    original_config = LoggerConfig(
        name="test_config",
        log_level="DEBUG",
        log_to_console=True,
        log_to_file=True,
        log_file="test.log",
        max_file_size=1024,
        backup_count=3
    )
    
    # Convert to dict and back
    config_dict = original_config.to_dict()
    new_config = LoggerConfig.from_dict(config_dict)
    
    # Verify all attributes match
    assert new_config.name == original_config.name
    assert new_config.log_level == original_config.log_level
    assert new_config.log_to_console == original_config.log_to_console
    assert new_config.log_to_file == original_config.log_to_file
    assert new_config.log_file == original_config.log_file
    assert new_config.max_file_size == original_config.max_file_size
    assert new_config.backup_count == original_config.backup_count


def test_config_file_operations():
    """Test saving and loading configuration to/from file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
        temp_path = temp_file.name
        
        # Create and save config
        config = LoggerConfig(
            name="file_config_test",
            log_level="WARNING",
            log_to_file=True,
            log_file="saved_config.log"
        )
        
        # Save to file
        config_dict = config.to_dict()
        json.dump(config_dict, temp_file, indent=2)
    
    try:
        # Load from file
        with open(temp_path, 'r') as f:
            loaded_dict = json.load(f)
        
        loaded_config = LoggerConfig.from_dict(loaded_dict)
        
        # Verify loaded config matches original
        assert loaded_config.name == "file_config_test"
        assert loaded_config.log_level == config.log_level
        assert loaded_config.log_to_file is True
        assert str(loaded_config.log_file) == "saved_config.log"
    
    finally:
        import os
        if os.path.exists(temp_path):
            os.unlink(temp_path)


if __name__ == "__main__":
    test_config_serialization()
    test_config_file_operations()
    print("Configuration tests passed!")
