import logging
import os

logger = logging.getLogger(__name__)
_handler = logging.StreamHandler()
_formatter = logging.Formatter("%(levelname)s %(message)s")
_handler.setFormatter(_formatter)
logger.addHandler(_handler)
logger.setLevel("INFO")

if os.environ.get("DEBUG"):
    logger.setLevel("DEBUG")
    logger.info("Logging at debug level")
