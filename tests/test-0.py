from nextlog import Logger
import logging

loki_url = "http://localhost:3100/api/prom/push"
labels = {
    'source' : 'localhost-x2'
}

logger = Logger(__name__,loki_url=loki_url,labels=labels)

logger.setLevel(logging.ERROR)
file_handler = logging.FileHandler('console2.log')
logger.addHandler(file_handler)

logger.error("Error log 1")
logger.error("Error log 2")
logger.critical("Critical log 1")
logger.critical("Critical log 2")
logger.error("Error log 3")
