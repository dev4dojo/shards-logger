import json
import logging

from shards.logger import JSONFormatter, configure_handler, get_formatter, get_logger


def test_json_formatter():
    formatter = JSONFormatter()
    assert isinstance(formatter, JSONFormatter)


def test_get_formatter_returns_json_and_default():
    assert isinstance(get_formatter(True), JSONFormatter)
    fmt = get_formatter(False)
    assert isinstance(fmt, logging.Formatter)
    assert not isinstance(fmt, JSONFormatter)


def test_json_formatter_format():
    formatter = JSONFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=10,
        msg="Test message",
        args=None,
        exc_info=None,
    )
    formatted_record = json.loads(formatter.format(record=record))
    print(formatted_record)  # For debugging purposes
    assert formatted_record["process"] == record.processName
    assert formatted_record["thread"] == record.threadName
    assert formatted_record["filename"] == record.pathname
    assert formatted_record["lineno"] == record.lineno
    assert formatted_record["level"] == record.levelname
    assert formatted_record["message"] == record.getMessage()


def test_get_logger_structured():
    logger = get_logger("test_structured", struct_log=True)
    handler = next(h for h in logger.handlers if isinstance(h, logging.StreamHandler))
    assert isinstance(handler.formatter, JSONFormatter)


def test_configure_handler_sets_formatter():
    handler = logging.StreamHandler()
    configure_handler(handler, struct_log=True)
    assert isinstance(handler.formatter, JSONFormatter)
    handler2 = logging.StreamHandler()
    configure_handler(handler2, struct_log=False)
    assert isinstance(handler2.formatter, logging.Formatter)
