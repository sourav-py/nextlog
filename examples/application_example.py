from nextlog import Logger
import logging
import time
import sys
import inspect

def caller_info():
    """
    This Function determines where a function was called from and in what context.
    It is not sutible for Production, as it is slow and resource intensive, just used to demonstrate how a sample
    program is closed depending on Nextlog errors
    
    Returns:
        dictionary: details about stack that called function
            file: The file name where the calling function is located.
            line: The line number in the file where the function call was made.
            function: The name of the function that made the call.
            code_context: The actual line of code that made the call.
    """
    
    # Get the current stack frame and go back one level
    stack = inspect.stack()
    # stack[2] gives you information about the caller of main_exit
    # stack[1] would be the main_exit
    caller_frame = stack[2]
    frame = caller_frame[1]
    info = {
        "file": caller_frame.filename,
        "line": caller_frame.lineno,
        "function": caller_frame.function,
        "code_context": caller_frame.code_context,
        "index": caller_frame.index
    }
    return info


def main_exit():
    """
    Example Exit function to simulate an application that imports Nextlog
    
    Example when logs successfully sent:
    
        Main Program: Exit called by:
        {'file': '/examples/application_example.py', 
        'line': 148, 
        'function': '<module>', 
        'code_context': ['main_exit()   # Stop the logger and finish sending logs\n'], 
        'index': 0}
        
    Example when logs have error:
    
        Main Program: Exit called by:
        {'file': 'nextlog/logger.py', 
        'line': 83, 
        'function': 'handle_error', 
        'code_context': ['self.exit_callback()  # Call the callback to signal an exit\n'], 
        'index': 0}
    
    """    
    info = caller_info() # Just for demo to show if application exits itself or if Nextlog exits due to error.
    logger.info(f"Main Program: Exit called by:\n\n {info}\n\n")    # Demonstrate what called main exit
    logger.stop()
    sys.exit(1)  # Exit the entire program


def setup_logger():
    """
    Sets up and configures a Nextlog Logger instance with specific settings for Loki and Redis.

    This function configures a Logger with connections to both a Loki server and a Redis server.
    It also sets up file and console handlers for the logger's output. The function initializes
    the Logger with predefined settings for URLs, hosts, and ports, and sets up logging handlers
    for both file and console output.

    Returns:
        Logger: An instance of the Nextlog Logger class configured with handlers, Loki integration,
                Redis connection, and an exit callback.

    Examples:
        >>> logger = setup_logger()
        >>> logger.info("This is a test log message")
    """
    
    #------------------------------------------------
    
    # Use Variables:
    
    '''
    loki_url = "http://localhost:3100/api/prom/push"
    redis_host='localhost' # Default is localhost
    redis_port=6379  # Default port is 6379
    detailed_logging=False #Default is False
    exit_callback=main_exit
    labels = {
        'source' : 'localhost-x2'
    }
    
    # Create Logger from variables

    logger = Logger(__name__,
                    loki_url=loki_url,
                    labels=labels,
                    redis_host=redis_host,
                    redis_port=redis_port,
                    exit_callback=exit_callback,
                    detailed_logging=detailed_logging)
    '''
    
    
    #------------------------------------------------
     
    # OR use Dictionary to config
    
    '''
    config = {
        'loki_url': "http://localhost:3100/api/prom/push",
        'redis_host': 'localhost',
        'redis_port': 6379,
        'detailed_logging': False,
        'exit_callback': main_exit,
        'labels': {'source': 'localhost-x2'}
    }
    
    # Create Logger from Dictionary

    logger = Logger(__name__, **config)
    '''
    #------------------------------------------------
    
    
    config = {
        'loki_url': "http://localhost:3100/api/prom/push",
        'redis_host': 'localhost',
        'redis_port': 6379,
        'detailed_logging': False,
        'exit_callback': main_exit,
        'labels': {'source': 'localhost-testing'}
    }
    
    # Create Logger from Dictionary

    logger = Logger(__name__, **config)
    
    
    # Set Log Level and handlers
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler('console2.log')
    console_handler = logging.StreamHandler()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Create Nextlog Logger Instance
logger = setup_logger()

# Simulate Logs from program 
logger.error("Main Program: Error log 1")
logger.error("Main Program: Error log 2")
logger.critical("Main Program: Critical log 1")
logger.critical("Main Program: Critical log 2")
logger.critical("Main Program: Critical log 3")   # Stop if there is an error
logger.error("Main Program: Error log 3")
logger.error("Main Program: Error log 4")
logger.error("Main Program: Error log 5")
time.sleep(5)   # Simulate work
main_exit()   # Stop the logger and finish sending logs
