# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-07-07

### Added
- Initial release of JMTLogger
- Multiprocessing-safe logging with queue-based handlers
- Thread-safe logging capabilities
- Configurable console and file output
- Rotating file handler with size limits and backup count
- Context manager support for automatic cleanup
- Exception logging with traceback preservation
- Comprehensive configuration management via LoggerConfig class
- Support for multiple log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Custom formatters for console and file output
- Example scripts for basic usage, multiprocessing, and threading
- Comprehensive test suite covering core functionality
- Type hints throughout the codebase
- PEP 8 compliant code formatting

### Features
- **JMTLogger class**: Main logger with multiprocessing support
- **LoggerConfig class**: Configuration management with validation
- **Custom handlers**: MultiprocessingHandler and SafeRotatingFileHandler
- **Easy integration**: Simple import and setup process
- **Performance optimized**: Minimal overhead in concurrent environments

### Documentation
- Complete README with usage examples
- Inline code documentation with type hints
- Example scripts demonstrating various use cases
- Test coverage for all major features
