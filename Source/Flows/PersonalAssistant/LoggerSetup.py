import logging
import sqlite3
import time

def initLogger():
	# Formats: https://stackoverflow.com/a/16759818
	#defaultFormat = "%(levelname)s:%(name)s:%(message)s"
	advancedFormat = "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
	logging.basicConfig(
		level = logging.INFO,
		format = advancedFormat,
		datefmt = "%Y-%m-%d %H:%M:%S",
		handlers = [
			logging.StreamHandler(),
			logging.FileHandler("Data/Log.log", "a"),
		]
	)
	sqliteHandler = SQLiteHandler(db = "Data/Log.db")
	sqliteHandler.setLevel(logging.INFO)
	logging.getLogger().addHandler(sqliteHandler)

class SQLiteHandler(logging.Handler):
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
		conn = sqlite3.connect(self.db)
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
		with sqlite3.connect(self.db) as conn:
			conn.execute(sql)
			conn.commit()  # not efficient, but hopefully thread-safe