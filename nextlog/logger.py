import logging
import requests
import threading
import redis
import time
import json
import datetime


dlogger = logging.Logger


class Logger:
    def __init__(self,name = __name__, level = logging.DEBUG,labels = {}, formatter = None, handler = None, loki_url = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        if formatter:
            self.logger.setFormatter(formatter)
        
        if handler:
            self.logger.addHandler(handler)

        self.loki_url = loki_url
        self.redis_server = redis.Redis(host='localhost',port=6379,db=0)
        self.running = True
        self.send_logs_thread = threading.Thread(target=self.send_logs)
        self.send_logs_thread.start()

    def send_logs(self):
        while self.running:
            time.sleep(1) 
            if self.loki_url:
                log_entry = self.redis_server.lindex('log_queue',1)
                if log_entry:
                    try:
                        response = self.api_call_loki(log_entry)
                        self.redis_server.lpop('log_queue')
                    except requests.exceptions.RequestException as e:
                        break
                else:
                    print("No log entry")

    def api_call_loki(self, redis_log_entry):

        log_entry = redis_log_entry.decode("utf-8").replace("'", '"')
        log_entry_json = json.loads(log_entry)

        payload = {
            "streams": [
                {
                    "labels": "{source=\"localhost3\"}",
                    "entries": [
                        {
                            "ts" : log_entry_json['timestamp'],
                            "line": f"[{log_entry_json['level']}] {log_entry_json['line']}"
                        }
                    ]            
                }

            ]
        }

        headers = {
            'Content-type': 'application/json'
        }

        payload = json.dumps(payload)
        print(payload)
        
        response = requests.post(self.loki_url,data=payload,headers=headers)
        return response



    def info(self,log_msg):
        self.push_to_redis(log_msg,"INFO")
        self.logger.info(log_msg)
    
    def debug(self,log_msg):
        self.push_to_redis(log_msg,"DEBUG")
        self.logger.debug(log_msg)
    
    def error(self,log_msg):
        self.push_to_redis(log_msg,"ERROR")
        self.logger.error(log_msg)
    
    def push_to_redis(self,log_msg,log_level):
        timestamp = datetime.datetime.utcnow()
        timestampstr = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        self.redis_server.rpush('log_queue',str({"level":log_level,"timestamp": timestampstr,'line':log_msg}))

    def stop(self):
        self.running = False
        self.send_logs_thread.join()


if __name__ == "__main__":

    loki_url = "http://localhost:3100/api/prom/push"

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler('cosole.log')
    file_handler.setFormatter(formatter)

    logger = Logger(name="main_logger",loki_url=loki_url,level=logging.DEBUG,handler=file_handler)
    
    
    logger.info("This is an infoo log!!")

    logger.debug("This is a debugg log!!")

    logger.error("This is an errorr log!!")
    


