import logging
#import requests
import threading
import redis
import time
import datetime

dlogger = logging.Logger


class NextLog:
    def __init__(self,logger_name = __name__, log_level = logging.DEBUG, loki_url = None):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(log_level)
        self.loki_url = loki_url
        self.redis_server = redis.Redis(host='localhost',port=6379,db=0)
        self.running = True
        self.send_logs_thread = threading.Thread(target=self.send_logs)
        self.send_logs_thread.start()

    def send_logs(self):
        while self.running:
            time.sleep(1)  # Adjust sleep time as needed
            if self.loki_url:
                log_entry = self.redis_server.brpop('log_queue')
                try:
                    #Process the log entry
                    #Send the log entry to loki as a payload of the post request.
                    pass
                except requests.exceptions.RequestException as e:
                    dlogger.error(e)
                    break

    def info(self,log_msg):
        self.redis_server.lpush('log_queue',str({'level':'info','timestamp': datetime.datetime.utcnow(),'line':log_msg}))
        self.logger.info(log_msg)
    
    def debug(self,log_msg):
        self.redis_server.lpush('log_queue',str({'level':'debug','timestamp': datetime.datetime.utcnow(),'line':log_msg}))
        self.logger.debug(log_msg)
    
    def error(self,log_msg):
        self.redis_server.lpush('log_queue',str({'level':'error','timestamp': datetime.datetime.utcnow(),'line':log_msg}))
        self.logger.error(log_msg)

    def stop(self):
        self.running = False
        self.send_logs_thread.join()


if __name__ == "__main__":
    loki_url = "http://localhost:3100/api/prom/push"
    logger = NextLog(loki_url=loki_url)
    """
    logger.info("This is an info log!!")

    logger.debug("This is a debug log!!")

    logger.error("This is an error log!!")
    """



