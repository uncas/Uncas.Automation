import logging

class ColoredLoggingFormatter(logging.Formatter):

    def __init__(self, formatString = None):
        defaultFormat = "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
        self.formatString = formatString if formatString else defaultFormat
        self.grey = "\x1b[38;20m"
        self.yellow = "\x1b[33;20m"
        self.red = "\x1b[31;20m"
        self.bold_red = "\x1b[31;1m"
        self.reset = "\x1b[0m"

    def getFormats(self):
        return {
            logging.DEBUG: self.grey + self.formatString + self.reset,
            logging.INFO: self.grey + self.formatString + self.reset,
            logging.WARNING: self.yellow + self.formatString + self.reset,
            logging.ERROR: self.red + self.formatString + self.reset,
            logging.CRITICAL: self.bold_red + self.formatString + self.reset
        }

    def format(self, record):
        log_fmt = self.getFormats().get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)