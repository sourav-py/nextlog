from nextlog import Logger
import logging

logger = Logger(name="my_logger",level=logging.DEBUG)

logger.debug("DEBUG log test 0")
logger.warning("WARNING log test 0")
logger.error("INFO log test 0")
logger.critical("CRITICAL log test 0")
