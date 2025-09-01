import logging

from shards.logger import get_logger


def test_get_logger():
    """
    Test the get_logger function to ensure it returns a logger with the correct name and level.
    """
    logger = get_logger("test_logger")
    assert isinstance(logger, logging.Logger), "Expected a logging.Logger instance"
    assert logger.name == "test_logger"
    assert len(logger.handlers) == 1  # Should have one handler by default


def test_get_logger_set_log_level():
    logger_info = get_logger(name="test_logger_info")
    assert logger_info.level == logging.INFO

    logger_debug = get_logger(name="test_logger", level=logging.DEBUG)
    assert logger_debug.level == logging.DEBUG


def test_get_logger_no_duplicate_handlers():
    logger = get_logger("test_no_duplicate")
    n_handlers = len(logger.handlers)
    logger2 = get_logger("test_no_duplicate")
    assert len(logger2.handlers) == n_handlers


def test_get_logger_adds_stream_handler(monkeypatch):
    # Remove handlers if any
    logger = get_logger("test_stream_handler")
    logger.handlers.clear()
    logger = get_logger("test_stream_handler")
    assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)
