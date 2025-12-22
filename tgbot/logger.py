import config
import logging


def setup_logger():
    formatter = logging.Formatter(
        fmt=config.LOGGER_FORMAT,
        datefmt=config.DATE_FORMAT
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)
