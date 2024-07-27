import logging
import requests
import threading
import redis
import json
import datetime
import sys

class Logger(logging.Logger):
    def __init__(self, *args, **kwargs):
        """
        Initializes the custom Logger with connection to Redis and optional Loki integration.
        
        Args:
            args: Variable length argument list passed to the logging.Logger base class.
            kwargs: Arbitrary keyword arguments containing:
                loki_url (str, optional): URL to the Loki server for sending log data.
                labels (dict, optional): Labels to attach to the log entries.
                redis_host (str, optional): Hostname of the Redis server. Defaults to 'localhost'.
                redis_port (int, optional): Port of the Redis server. Defaults to 6379.
                exit_callback (callable, optional): Callback function to execute on critical failure.
                detailed_logging (bool, optional): Enable detailed error messages. Defaults to False.
        """
        super().__init__(*args)
        self.loki_url = kwargs.get('loki_url', None)
        self.labels = kwargs.get('labels', {})
        redis_host = kwargs.get('redis_host', 'localhost')
        redis_port = kwargs.get('redis_port', 6379)
        self.exit_callback = kwargs.get('exit_callback', None)
        self.redis_server = redis.Redis(host=redis_host, port=redis_port, db=0)
        self.detailed_logging = kwargs.get('detailed_logging', False)
        self.stop_event = threading.Event()
        self.send_logs_thread = threading.Thread(target=self.send_logs)
        self.error_counter = 0
        self.max_errors = 5
        self.send_logs_thread.start()

    def send_logs(self):
        """
        Continuously monitors and sends logs from the Redis queue to Loki until stopped.
        """
        try:
            while not self.stop_event.is_set():
                log_entry = self.redis_server.blpop('log_queue', 5)
                if log_entry and self.loki_url:
                    self.process_log_entry(log_entry)
                if self.stop_event.is_set():
                    break  # Ensure immediate termination if the event is set
        except Exception as e:
            self.error("Fatal error in send_logs: {}".format(str(e)))

    def process_log_entry(self, log_entry):
        """
        Processes and sends a single log entry to Loki.
        
        Args:
            log_entry (tuple): A tuple containing the Redis queue key and the log entry.
        """
        _, log_entry = log_entry
        log_entry_str = log_entry.decode('utf-8')
        try:
            response = self.api_call_loki(log_entry_str)
            if response.status_code != 204:
                raise requests.exceptions.RequestException(response.text)
            self.error_counter = 0
        except requests.exceptions.RequestException as e:
            self.handle_error(e)

    def handle_error(self, error):
        """
        Handles errors occurred during log sending, including counting and reacting to consecutive errors.
        
        Args:
            error (Exception): The exception that occurred during the logging process.
        """
        self.error("Nextlog: Failed to send logs: {}".format(error if self.detailed_logging else error.__class__.__name__))
        self.error_counter += 1
        if self.error_counter >= self.max_errors:
            self.error("Nextlog: Maximum consecutive errors reached.")
            if threading.current_thread() == self.send_logs_thread:
                if self.exit_callback:
                    self.error("Nextlog: Exiting with Callback.")
                    self.exit_callback()  # Call the callback to signal an exit
            else:
                sys.exit(1)  # Exit the program from a non-logging thread

    def api_call_loki(self, redis_log_entry):
        """
        Sends a formatted log entry to the Loki server.
        
        Args:
            redis_log_entry (str): The JSON string of the log entry to be sent.
        
        Returns:
            requests.Response: The response object from the Loki server.
        """
        try:
            log_entry_json = json.loads(redis_log_entry)
        except json.JSONDecodeError as e:
            self.error(f"Nextlog: JSON decode error: {e} in entry: {redis_log_entry}")
            return None
        payload = {
            "streams": [
                {
                    "labels": self.get_labels_string(self.labels),
                    "entries": [
                        {
                            "ts": log_entry_json['timestamp'],
                            "line": f"[{log_entry_json['level']}] {log_entry_json['line']}"
                        }
                    ]
                }
            ]
        }
        headers = {'Content-type': 'application/json'}
        payload = json.dumps(payload)
        response = requests.post(self.loki_url, data=payload, headers=headers)
        return response

    def get_labels_string(self, labels_map):
        """
        Formats the labels into a string that can be sent to Loki.
        
        Args:
            labels_map (dict): A dictionary of labels.
        
        Returns:
            str: A string representation of the labels formatted for Loki.
        """
        labels_string = "{"
        for key, value in labels_map.items():
            labels_string += f'{key}="{value}", '
        labels_string = labels_string.rstrip(", ")
        labels_string += "}"
        return labels_string

    def info(self, msg):
        self.push_to_redis(msg, "INFO")
        super().info(msg)

    def debug(self, msg):
        self.push_to_redis(msg, "DEBUG")
        super().debug(msg)

    def warning(self, msg):
        self.push_to_redis(msg, "WARNING")
        super().warning(msg)

    def error(self, msg):
        self.push_to_redis(msg, "ERROR")
        super().error(msg)

    def critical(self, msg):
        self.push_to_redis(msg, "CRITICAL")
        super().critical(msg)

    def push_to_redis(self, msg, log_level):
        """
        Pushes a log message into the Redis queue.
        
        Args:
            msg (str): The message to log.
            log_level (str): The logging level of the message.
        """
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        log_entry = json.dumps({"level": log_level, "timestamp": timestamp, 'line': msg})
        self.redis_server.rpush('log_queue', log_entry)

    def stop(self):
        """
        Stops the logging process and ensures all threads are cleanly shutdown.
        """
        self.stop_event.set()
        if threading.current_thread() != self.send_logs_thread:
            self.info("Nextlog: Stopping logging thread.")
            self.send_logs_thread.join()
        self.info("Nextlog: All logs have been sent and the logger is stopping.")