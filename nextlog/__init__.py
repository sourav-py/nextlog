import logging

class Logger:
    def __init__(self,log_level=logging.INFO):
        
        #Create logger with the name set to module name
        #and level set to argument value 
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        #Add handler to output logs to console
        ch = logging.StreamHandler()
        self.logger.addHandler(ch)
    
    def info(self,log_message):
        self.logger.info(log_message)
    
    def debug(self,log_message):
        self.logger.debug(log_message)

    def error(self,log_message):
        self.logger.error(log_message)

logger = Logger()
logger.error("Log message!!")


