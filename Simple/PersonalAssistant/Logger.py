class Logger:
	DEBUG = '\033[96m'
	INFO = '\033[92m'
	WARNING = '\033[93m'
	ERROR = '\033[91m'
	ENDC = '\033[0m'
	
	def __init__(self):
		import os
		from dotenv import load_dotenv # type: ignore
		load_dotenv()
		self.logLevel = os.getenv('LogLevel', 'WARNING')
		self.info("Started with log level " + self.logLevel)
    
	def error(self, message):
		if self.logLevel == 'Error' or self.logLevel == 'WARNING' or self.logLevel == 'INFO' or self.logLevel == 'DEBUG':
			print(self.ERROR, "ERROR: ", message, self.ENDC)

	def warning(self, message):
		if self.logLevel == 'WARNING' or self.logLevel == 'INFO' or self.logLevel == 'DEBUG':
			print(self.WARNING, "WARNING: ", message, self.ENDC)

	def info(self, message):
		if self.logLevel == 'INFO' or self.logLevel == 'DEBUG':
			print(self.INFO, "INFO: ", message, self.ENDC)

	def debug(self, message):
		if self.logLevel == 'DEBUG':
			print(self.DEBUG, "DEBUG: ", message, self.ENDC)
