class foreground:
    BLACK   = '\033[30m'
    RED     = '\033[31m'
    GREEN   = '\033[32m'
    YELLOW  = '\033[33m'
    BLUE    = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN    = '\033[36m'
    WHITE   = '\033[37m'
    RESET   = '\033[39m'

class background:
    BLACK   = '\033[40m'
    RED     = '\033[41m'
    GREEN   = '\033[42m'
    YELLOW  = '\033[43m'
    BLUE    = '\033[44m'
    MAGENTA = '\033[45m'
    CYAN    = '\033[46m'
    WHITE   = '\033[47m'
    RESET   = '\033[49m'

class style:
    BRIGHT    = '\033[1m'
    DIM       = '\033[2m'
    NORMAL    = '\033[22m'
    RESET_ALL = '\033[0m'

class Logger:
	DEBUG = background.BLUE + foreground.WHITE
	INFO = background.BLACK + foreground.YELLOW
	WARNING = background.WHITE + foreground.YELLOW
	ERROR = background.YELLOW + foreground.RED
	RESET = style.RESET_ALL
	
	def __init__(self):
		import os
		from dotenv import load_dotenv # type: ignore
		load_dotenv()
		self.logLevel = os.getenv('LogLevel', 'WARNING')
		self.info("Started with log level " + self.logLevel)
    
	def error(self, message):
		if self.logLevel == 'Error' or self.logLevel == 'WARNING' or self.logLevel == 'INFO' or self.logLevel == 'DEBUG':
			print(self.ERROR, "ERROR: ", message, self.RESET)

	def warning(self, message):
		if self.logLevel == 'WARNING' or self.logLevel == 'INFO' or self.logLevel == 'DEBUG':
			print(self.WARNING, "WARNING: ", message, self.RESET)

	def info(self, message):
		if self.logLevel == 'INFO' or self.logLevel == 'DEBUG':
			print(self.INFO, "INFO: ", message, self.RESET)

	def debug(self, message):
		if self.logLevel == 'DEBUG':
			print(self.DEBUG, "DEBUG: ", message, self.RESET)
