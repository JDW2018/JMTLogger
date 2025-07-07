# Copilot Instructions

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

This is a JMTLogger project designed for multiprocessing environments. The project should:

- Support thread-safe and process-safe logging
- Be importable as a package into other projects
- Provide configurable output destinations (console, file, or both)
- Follow Python logging best practices
- Include proper documentation and examples
- Use type hints throughout the codebase
- Follow PEP 8 style guidelines

## Project Structure
```
src/jmtlogger/          # Main package directory
├── __init__.py         # Package initialization
├── core.py            # JMTLogger main class
├── config.py          # LoggerConfig class
└── handlers.py        # Custom multiprocessing handlers

examples/              # Usage examples
├── basic_usage.py
├── multiprocess.py
├── threading.py
└── import_example.py

tests/                 # Test suite
├── test_core.py
├── test_config.py
└── test_multiprocess.py
```

## Key Components
- **JMTLogger class**: Main multiprocessing-safe logger implementation
- **LoggerConfig class**: Configuration management with validation
- **Custom handlers**: MultiprocessingHandler and SafeRotatingFileHandler
- **Thread/process coordination**: Queue-based logging for safety
- **Example usage scripts**: Demonstrating various use cases

## Import Usage
```python
from jmtlogger import JMTLogger, LoggerConfig
```
