# nextlog
This is a `python` logging library which asynchronously dispatches logs to monitoring services like loki.
It uses the OOTB python logging library as its base.<br>
Whenever the logger statement - `logger.info()` / `logger.debug()` / `logger.error()` etc. gets executed, the log is pushed onto a `redis` queue.<br>
A process running on separate thread will keep dispatching those logs to the specified loki endpoint.

## Features
- **Seamless Integration**: nextlog builds upon the Python logging library, so its usage is similar and familiar.
- **Async Dispatch**: Logs are asynchronously dispatched to monitoring services like Loki, ensuring minimal impact on the main code flow.
- **Redis Backup**: Utilizes Redis to temporarily store logs in case the monitoring service (e.g., Loki) is unavailable.

## Setup
### Install the library 
`pip3 install nextlog`
### Setup redis server
`docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest`

## Usage

```
from nextlog import Logger
import logging

# Define labels for logs
labels = {'source': 'localhost'}

# Loki server URL
loki_url = "http://localhost:3100/api/prom/push"

# Initialize nextlog logger
logger = Logger(__name__,loki_url=loki_url,labels=labels)

# Apply preferred logging configs
logger.setLevel(logging.ERROR)
file_handler = logging.FileHandler('console2.log')
logger.addHandler(file_handler)

# Log messages
logger.error("Error log 1")
logger.error("Error log 2")
logger.critical("Critical log 1")
logger.critical("Critical log 2")
logger.error("Error log 3")


```
