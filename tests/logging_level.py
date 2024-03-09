import logging

# Create logger object
logger = logging.getLogger("my_logger")

# Set logging level to output logs for all levels
logger.setLevel(logging.DEBUG)

# Define the formatter for log messages
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a file handler to save logs to a file
file_handler = logging.FileHandler('console.log')
#file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Additional attributes
logger.prop1 = 'value1'
logger.prop2 = 'value2'

# Example usage
logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')
