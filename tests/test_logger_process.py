import multiprocessing as mp
from queue import Empty as EmptyQueue

from shards.logger import get_logger


class ProcessLogger(mp.Process):
    """
    A process that initializes a logger and listens for log messages.
    """

    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        logger = get_logger(name="process_logger", queue=self.queue)
        logger.info("Process started")
        # Simulate some work
        for i in range(5):
            logger.info(f"Processing item {i}")
        logger.info("Process finished")


def test_process_logger():
    """
    Test the ProcessLogger to ensure it can log messages correctly.
    """
    log_queue = mp.Queue()
    process = ProcessLogger(queue=log_queue)
    process.start()
    process.join()

    # Collect log messages from the queue
    messages = []
    try:
        while True:
            record = log_queue.get_nowait()
            messages.append(record)
    except EmptyQueue:
        pass

    # Check that expected log messages are present
    log_texts = [getattr(record, "msg", str(record)) for record in messages]
    assert any("Process started" in msg for msg in log_texts)
    assert any("Processing item 0" in msg for msg in log_texts)
    assert any("Process finished" in msg for msg in log_texts)

    assert len(messages) == 7  # 1 start + 5 processing + 1 finish
