# Logger

A structured and extensible logging utility for Python applications. This module simplifies the setup of both traditional and structured (JSON-based) logging using standard Python logging facilities. It supports asynchronous logging via queues and listeners, making it suitable for multiprocessing or performance-sensitive applications.

## Features

* Console and queue-based logging
* Optional structured JSON logs
* Configurable log levels
* Asynchronous logging with `QueueHandler`
* Extendable for file-based logging (placeholder included)

## Installation

No external dependencies beyond the Python standard library.

## Usage

```python
from logger import get_logger
from queue import Queue

# Standard text logging
logger = get_logger("myapp")
logger.info("Hello, log!")

# Structured logging (JSON format)
logger = get_logger("myapp_struct", struct_log=True)
logger.warning("This is structured")

# Logging with a queue (useful for multiprocessing)
log_queue = Queue()
logger = get_logger("queued_logger", queue=log_queue)
logger.debug("Message to log queue")
```

## Structured Logging

is a great way to improve the traceability, searchability, and analysis of logs, especially in larger applications. By logging in a structured format (e.g., JSON), you can easily integrate with log aggregators, perform automated parsing, and analyze logs more efficiently.

## Advantages of This Approach

- **Centralized Logging**: Logs from multiple processes are handled in a single place.
- **Performance**: Log processing is offloaded from worker processes, avoiding contention for resources.
- **Scalability**: Easily extendable to include more processes or handlers (e.g., database or cloud logging).
- **Separation of Concerns**: Worker processes focus on logging, while the main process handles log processing.

## Common Issues and Debugging

- **Deadlocks**: Ensure that `QueueListener.stop()` is always called to prevent hanging processes.
- **Serialization Errors**: Log records are serialized using pickle. Custom objects in log messages should be serializable.
- **Performance**: For high-throughput systems, monitor the queue size to avoid bottlenecks.


## Development Notes

* The module includes a `JSONFormatter` class for structured logging.

## TODO

* [ ] Add file logging support
* [ ] Add more usage samples in this README and inline

