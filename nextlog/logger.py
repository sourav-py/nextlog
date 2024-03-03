import logging
import requests
import threading
import redis
import time
import json
import datetime


dlogger = logging.Logger


class NextLog:
    def __init__(self,logger_name = __name__, log_level = logging.INFO, loki_url = None):
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
                    response = self.api_call_loki(log_entry)
                except requests.exceptions.RequestException as e:
                    dlogger.error(e)
                    break

    def api_call_loki(self, redis_log_entry):

        log_entry = redis_log_entry[1].decode("utf-8").replace("'", '"')
        log_entry_json = json.loads(log_entry)

        payload = {
            'streams': [
                {
                    'labels': '{source=\"localhost\"}',
                    'entries': [
                        {
                            'ts' : log_entry_json['timestamp'],
                            'line': f"[{log_entry_json['level']}] {log_entry_json['line']}"
                        }
                    ]            
                }

            ]
        }

        headers = {
            'Content-type': 'application/json'
        }

        payload = json.dumps(payload)
        
        response = requests.post(self.loki_url,data=payload,headers=headers)
        return response



    def info(self,log_msg):
        self.redis_server.lpush('log_queue',str({"level":'info',"timestamp": str(datetime.datetime.utcnow()),'line':log_msg}))
        self.logger.info(log_msg)
    
    def debug(self,log_msg):
        self.redis_server.lpush('log_queue',str({"level":'debug',"timestamp": str(datetime.datetime.utcnow()),'line':log_msg}))
        self.logger.debug(log_msg)
    
    def error(self,log_msg):
        self.redis_server.lpush('log_queue',str({"level":'error',"timestamp": str(datetime.datetime.utcnow()),'line':log_msg}))
        self.logger.error(log_msg)

    def stop(self):
        self.running = False
        self.send_logs_thread.join()


if __name__ == "__main__":
    loki_url = "http://localhost:3100/loki/api/v1/push"
    logger = NextLog(loki_url=loki_url)
    
    logger.info("This is an infoo log!!")

    logger.debug("This is a debugg log!!")

    logger.error("This is an errorr log!!")
    



