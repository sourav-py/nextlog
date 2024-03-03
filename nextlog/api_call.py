import requests
import json
import redis

def api_call_loki(redis_log_entry,loki_url):

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

    payload = json.dumps(payload)
    
    #Send request
    #response = requests.(...)
    #return response

