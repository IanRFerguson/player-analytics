import logging
import os
import sys

from colorlog import ColoredFormatter

#####


pipeline_logger = logging.getLogger(__name__)
_handler = logging.StreamHandler(sys.stdout)
_formatter = ColoredFormatter(
    "%(log_color)s%(levelname)s%(reset)s %(message)s",
    reset=True,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    },
    style="%",
)

_handler.setFormatter(_formatter)
pipeline_logger.addHandler(_handler)
pipeline_logger.setLevel("INFO")


if os.environ.get("DEBUG_LOG") == "true":
    pipeline_logger.setLevel("DEBUG")
    pipeline_logger.debug("Logging at debug level")
