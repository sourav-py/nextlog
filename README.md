# [nextlog](https://pypi.org/project/nextlog/)
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

---

## Setup test enviroment from local source
### Download the library from Git Repo
1. Download the zip file from Git Repo
2. Unzip
3. Go to root folder for `nextlog`
### Setup Virtual Enviroment and install nextlog locally
1. `python -m venv venv`
2. `source venv/bin/activate`  # On Windows use `venv\Scripts\activate`
3. `pip install -e .` This installs nextlog via the nextlog folder rather than though pip
4. Local Nextlog should be importable via `from nextlog import Logger`

---

## Examples

### Check out the [Examples](examples) folder for two examples.

The [basic example](examples/basic_example.py) is a simple way to use Nextlog to send logs, but does not use optional features like exit methods and shared flags that would exist in an application

The [application example](examples/application_example.py) is a quick start example to use Nextlog in a more robust application. This allows Nextlog to exit the main application if there are errors in logging setup (like connecting to redis or grafana) and more robust commenting for options.

## Basic Usage

```
from nextlog import Logger
import logging

loki_url = "http://localhost:3100/api/prom/push"
redis_host='localhost' # Default is localhost
redis_port=6379  # Default port is 6379

labels = {
    'source' : 'localhost-x2'
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
logger.stop() #Stop the logger and finish sending logs


```
