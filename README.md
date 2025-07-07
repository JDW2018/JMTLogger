# JMTLogger

A robust, thread-safe and process-safe logging engine designed for Python applications that require standardized logging across multiple processes and threads.

## Features

- **Multiprocessing Support**: Thread-safe and process-safe logging using queue-based handlers
- **Configurable Output**: Console, file, or both output destinations
- **Colored Console Output**: Automatic color coding for different log levels on Windows and Linux
- **Standardized Interface**: Consistent logging across all projects
- **Easy Integration**: Simple import and setup
- **Performance Optimized**: Minimal overhead in concurrent environments
- **Exception Handling**: Proper exception logging with traceback preservation
- **File Rotation**: Configurable rotating file handlers with size limits

## Installation

### From PyPI (once published)
```bash
pip install jmtlogger
```

### From Source
```bash
git clone https://github.com/JDW2018/JMTLogger.git
cd JMTLogger
pip install -e .
```

### For Development
```bash
git clone https://github.com/JDW2018/JMTLogger.git
cd JMTLogger
pip install -e .[dev]
```

## Quick Start

```python
from jmtlogger import JMTLogger

# Initialize logger with colored output (default)
logger = JMTLogger(
    name="my_app",
    log_to_console=True,
    log_to_file=True,
    log_file="app.log",
    log_level="INFO",
    use_colors=True  # Enable colored console output (default: True)
)

# Use in your application
logger.info("Application started")  # Green text
logger.warning("Warning message")   # Yellow text
logger.error("An error occurred")   # Red text
logger.close()  # Clean up when done
```

## Color Support

JMTLogger automatically detects terminal color support and applies colors to console output:

- **DEBUG**: Cyan
- **INFO**: Green  
- **WARNING**: Yellow
- **ERROR**: Red
- **CRITICAL**: Magenta

Colors work on:
- Windows 10+ (with ANSI support)
- Linux terminals
- macOS terminals
- Most modern terminal emulators

To disable colors:
```python
logger = JMTLogger(name="my_app", use_colors=False)
```

## Advanced Configuration

```python
from jmtlogger import JMTLogger, LoggerConfig

# Using configuration object
config = LoggerConfig(
    name="advanced_app",
    log_level="DEBUG",
    log_to_console=True,
    log_to_file=True,
    log_file="logs/app.log",
    max_file_size=50 * 1024 * 1024,  # 50MB
    backup_count=10,
    use_colors=True,  # Enable colored console output
    console_format="%(levelname)s: %(message)s",
    file_format="%(asctime)s - %(name)s - %(levelname)s - %(processName)s - %(threadName)s - %(funcName)s:%(lineno)d - %(message)s"
)

logger = JMTLogger(config=config)
```

## Multiprocessing Example

```python
import multiprocessing
from jmtlogger import JMTLogger

def worker_function(worker_id):
    logger = JMTLogger(
        name="worker_logger",
        log_to_console=True,
        log_to_file=True,
        log_file="worker.log"
    )
    
    logger.info(f"Worker {worker_id} starting")
    # Your work here
    logger.info(f"Worker {worker_id} finished")
    logger.close()

if __name__ == "__main__":
    processes = []
    for i in range(4):
        p = multiprocessing.Process(target=worker_function, args=(i,))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
```

## Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | str | "jmt_logger" | Logger name |
| `log_level` | str/int | "INFO" | Logging level |
| `log_to_console` | bool | True | Enable console output |
| `log_to_file` | bool | False | Enable file output |
| `log_file` | str/Path | None | Log file path |
| `log_dir` | str/Path | None | Log directory (auto-generates filename) |
| `max_file_size` | int | 10MB | Max file size before rotation |
| `backup_count` | int | 5 | Number of backup files to keep |
| `console_format` | str | Standard format | Console log format |
| `file_format` | str | Detailed format | File log format |
| `date_format` | str | "%Y-%m-%d %H:%M:%S" | Date format |

## Project Structure

```
src/
├── __init__.py          # Package initialization
├── config.py            # Configuration management
├── core.py              # Core logging engine
└── handlers.py          # Custom handlers for multiprocessing

examples/
├── basic_usage.py       # Basic usage example
├── multiprocess.py      # Multiprocessing example
├── threading.py         # Threading example
└── import_example.py    # Import in other projects example

tests/
├── test_core.py         # Core functionality tests
├── test_multiprocess.py # Multiprocessing tests
└── test_config.py       # Configuration tests
```

## VS Code Tasks

This project includes VS Code tasks for easy development:

- **Install Development Dependencies**: Install the package in development mode
- **Run Basic Example**: Test basic logging functionality
- **Run Multiprocessing Example**: Test multiprocessing logging
- **Run Threading Example**: Test threading logging
- **Run Import Example**: Test importing in other projects
- **Run All Manual Tests**: Execute all test files

Access these through VS Code's Command Palette: `Ctrl+Shift+P` → "Tasks: Run Task"

## API Reference

### JMTLogger Class

```python
JMTLogger(name, config=None, **kwargs)
```

**Methods:**
- `debug(message, *args, **kwargs)`: Log debug message
- `info(message, *args, **kwargs)`: Log info message
- `warning(message, *args, **kwargs)`: Log warning message
- `error(message, *args, **kwargs)`: Log error message
- `critical(message, *args, **kwargs)`: Log critical message
- `exception(message, *args, **kwargs)`: Log exception with traceback
- `set_level(level)`: Change logging level
- `get_level()`: Get current logging level
- `is_enabled_for(level)`: Check if level is enabled
- `close()`: Close all handlers and clean up

### LoggerConfig Class

```python
LoggerConfig(name, log_level, log_to_console, log_to_file, ...)
```

**Methods:**
- `from_dict(config_dict)`: Create from dictionary
- `to_dict()`: Convert to dictionary

## Best Practices

1. **Always close loggers**: Use `logger.close()` or context managers
2. **Use appropriate log levels**: DEBUG for development, INFO for production
3. **Configure file rotation**: Set reasonable `max_file_size` and `backup_count`
4. **Process-specific loggers**: Create separate loggers for different processes
5. **Exception logging**: Use `logger.exception()` in except blocks

## Threading and Multiprocessing Safety

This logger is designed to be safe for use across multiple threads and processes:

- **Thread Safety**: Uses thread-safe queues and locks
- **Process Safety**: Each process can safely write to shared log files
- **Queue-based**: Log records are queued to prevent blocking
- **Handler Isolation**: Each handler runs in its own thread

## Development

1. Clone the repository
2. Install development dependencies: `pip install -e .[dev]`
3. Run examples: `python examples/basic_usage.py`
4. Run tests: `python tests/test_config.py`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all examples work
6. Submit a pull request

## License

**Non-Commercial Use License**

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0).

**You are free to:**
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material

**Under the following terms:**
- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made
- **NonCommercial** — You may not use the material for commercial purposes

For commercial licensing options, please contact JMTechnical Group.

See the [LICENSE](LICENSE) file for full details or visit [CC BY-NC 4.0](http://creativecommons.org/licenses/by-nc/4.0/).
