"""
Logging Module

TODO: Add samples how to use this module
"""

import json
import logging
from logging import Formatter, Handler, LogRecord, StreamHandler
from logging.handlers import QueueHandler
from queue import Queue

DEFAULT_LOGGING_FORMAT = (
    "%(asctime)s.%(msecs)03d [%(levelname)s] (%(name)s:%(lineno)s) %(message)s"
)
CUSTOM_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for logging."""

    def __init__(self, fmt=None, datefmt: str = CUSTOM_DATETIME_FORMAT):
        super().__init__(fmt, datefmt)

    def format(self, record: LogRecord) -> str:
        log_obj = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "process": record.processName,
            "thread": record.threadName,
            "filename": record.pathname,
            "lineno": record.lineno,
        }
        return json.dumps(log_obj)


def get_formatter(struct_log: bool = False):
    """
    Returns the appropriate formatter based on the configuration.

    Args:
        struct_log (bool): If True, use JSONFormatter for structured logging.
                           Otherwise, use the default text formatter.

    Returns:
        logging.Formatter: Configured formatter instance.
    """
    return (
        JSONFormatter()
        if struct_log
        else Formatter(fmt=DEFAULT_LOGGING_FORMAT, datefmt=CUSTOM_DATETIME_FORMAT)
    )


def configure_handler(handler: Handler, struct_log: bool = False):
    """
    Configures a handler with the appropriate formatter.

    Args:
        handler (Handler): The logging handler to configure.
        struct_log (bool): If True, use JSONFormatter for structured logging.
                           Otherwise, use the default text formatter.
    """
    handler.setFormatter(get_formatter(struct_log))


def get_logger(name: str, queue: Queue = None, level=logging.INFO, struct_log=False):
    """
    Creates and configures a logger with a queue handler.

    Args:
        name (str): The name of the logger.
        queue (queue.Queue): The queue to which log messages will be sent.
        level (int, optional): The logging level. Defaults to logging.INFO.
        struct_log (bool, optional): Whether to use structured logging. Defaults to False.

    Returns:
        logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:  # Prevent duplicate handlers
        if queue:
            queue_handler = QueueHandler(queue)
            configure_handler(queue_handler, struct_log)
            logger.addHandler(queue_handler)
        else:
            console_handler = StreamHandler()
            configure_handler(console_handler, struct_log)
            logger.addHandler(console_handler)
    return logger
