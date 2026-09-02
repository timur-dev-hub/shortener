import logging
from logging.handlers import TimedRotatingFileHandler


def setup_logging():

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # HANDLERS

    # CONSOLE
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # FILE
    rotating_file_handler = TimedRotatingFileHandler(
        'app.log',
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8")

    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s | %(filename)s:%(lineno)d | %(message)s')
    rotating_file_handler.setFormatter(file_formatter)
    root_logger.addHandler(rotating_file_handler)

