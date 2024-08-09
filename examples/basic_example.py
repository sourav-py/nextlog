from nextlog import Logger
import logging

loki_url = "http://localhost:3100/api/prom/push"
redis_host='localhost' # Default is localhost
redis_port=6379  # Default port is 6379

labels = {
    'source' : 'localhost-x11'
}

logger = Logger(__name__,loki_url=loki_url,labels=labels)

logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('console2.log')
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.error("Error log 1")
logger.error("Error log 2")
logger.critical("Critical log 1")
logger.critical("Critical log 2")
logger.error("Error log 3")
logger.error("Error log 4")
logger.error("Error log 5")
logger.error("Error log 6")
logger.error("Error log 7")
logger.error("Error log 8")
logger.error("Error log 9")

logger.stop() #Stop the logger and finish sending logs

"""
    In order to terminate the whole logging process immediately,
    utilize the following function:

    logger.hard_stop()
"""