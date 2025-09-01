import logging
import multiprocessing as mp
import queue
import re

from shards.logger import get_logger

RE_LOG_FORMAT = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3} \[\w+\] \(\w+:\d+\) .*"


def test_get_logger_adds_queue_handler():
    q = queue.Queue()
    logger = get_logger("test_queue_handler", queue=q)
    assert any(isinstance(h, logging.handlers.QueueHandler) for h in logger.handlers)
    logger.info("test message")
    record = q.get(timeout=2)
    assert hasattr(record, "msg")
    assert re.match(RE_LOG_FORMAT, record.msg)


def test_logger_logs_to_queue():
    q = mp.Queue()
    logger = get_logger("test_mp_queue", queue=q)
    logger.info("test message")
    record = q.get(timeout=2)
    assert hasattr(record, "msg")
    assert re.match(RE_LOG_FORMAT, record.msg)
