import logging
import sqlite3
import time

def initLogger():
	# Formats: https://stackoverflow.com/a/16759818
	#defaultFormat = "%(levelname)s:%(name)s:%(message)s"
	advancedFormat = "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
	logging.basicConfig(
		level = logging.DEBUG,
		format = advancedFormat,
		datefmt = "%Y-%m-%d %H:%M:%S",
		handlers = [
			SQLiteLoggingHandler(db = "Data/Log.db"),
			#logging.StreamHandler(),
			#logging.FileHandler("Data/Log.log", "a"),
		]
	)

# Derived from https://gist.github.com/gormih/09d18e7da67271b79b6cb3537ebfa4f3
class SQLiteLoggingHandler(logging.Handler):
	def initial_sql(self):
		return """CREATE TABLE IF NOT EXISTS log(
		Created TEXT,
		Source TEXT,
		LogLevel INT,
		LogLevelName TEXT,
		Message TEXT,
		Args TEXT,
		Module TEXT,
		FuncName TEXT,
		LineNo INT,
		Exception TEXT,
		Process INT,
		Thread TEXT,
		ThreadName TEXT,
		TimeStamp INTEGER
	)"""

	def insertion_sql(self):
		return """INSERT INTO log(
		Created,
		Source,
		LogLevel,
		LogLevelName,
		Message,
		Args,
		Module,
		FuncName,
		LineNo,
		Exception,
		Process,
		Thread,
		ThreadName,
		TimeStamp
	)
	VALUES (
		'%(dbtime)s',
		'%(name)s',
		%(levelno)d,
		'%(levelname)s',
		'%(msg)s',
		'%(args)s',
		'%(module)s',
		'%(funcName)s',
		%(lineno)d,
		'%(exc_text)s',
		%(process)d,
		'%(thread)s',
		'%(threadName)s',
		%(timestamp)d
	);
	"""

	def __init__(self, db='app.db'):
		logging.Handler.__init__(self)
		self.db = db
		with sqlite3.connect(self.db) as conn:
			conn.execute(self.initial_sql())
			conn.commit()

	def format_time(self, record):
		"""
		Create a time stamp
		"""
		record.dbtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(record.created))
		record.timestamp = record.created

	def emit(self, record):
		self.format(record)
		self.format_time(record)
		if record.exc_info:  # for exceptions
			record.exc_text = logging._defaultFormatter.formatException(record.exc_info)
		else:
			record.exc_text = ""

        # Insert the log record
		sql = self.insertion_sql() % record.__dict__
		try:
			with sqlite3.connect(self.db) as conn:
				conn.execute(sql)
				conn.commit()  # not efficient, but hopefully thread-safe
		except Exception as e:
			print(e)