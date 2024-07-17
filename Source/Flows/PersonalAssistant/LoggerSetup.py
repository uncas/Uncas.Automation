import logging
import sqlite3

def initLogger():
	# Formats: https://stackoverflow.com/a/16759818
	#defaultFormat = "%(levelname)s:%(name)s:%(message)s"
	advancedFormat = "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
	logging.basicConfig(
		level = logging.INFO,
		format = advancedFormat,
		datefmt = "%Y-%m-%d %H:%M:%S",
		handlers = [
			SQLiteLoggingHandler(db = "Data/Log.db"),
			#logging.StreamHandler(),
			#logging.FileHandler("Data/Log.log", "a"),
		]
	)

class SQLiteLoggingHandler(logging.Handler):
	# Derived from https://gist.github.com/gormih/09d18e7da67271b79b6cb3537ebfa4f3

	def __init__(self, db='app.db'):
		logging.Handler.__init__(self)
		self.db = db
		sql = """
			CREATE TABLE IF NOT EXISTS log (
				Created TEXT, Source TEXT, LogLevel INT, LogLevelName TEXT, Message TEXT,
				Args TEXT, Module TEXT, FuncName TEXT, LineNo INT, Exception TEXT,
				Process INT, Thread TEXT, ThreadName TEXT, TimeStamp INTEGER
			);"""
		with sqlite3.connect(self.db) as conn:
			conn.execute(sql)
			conn.commit()

	def format_time(self, record):
		import datetime
		record.dbtime = datetime.datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S.%f")
		record.timestamp = record.created

	def emit(self, record):
		self.format(record)
		self.format_time(record)
		if record.exc_info:  # for exceptions
			record.exc_text = logging._defaultFormatter.formatException(record.exc_info)
		else:
			record.exc_text = ""
		sql = """
			INSERT INTO log (
				Created, Source, LogLevel, LogLevelName, Message,
				Args, Module, FuncName, LineNo, Exception, 
				Process, Thread, ThreadName, TimeStamp
			)
			VALUES (
				?, ?, ?, ?, ?, 
				?, ?, ?, ?, ?, 
				?, ?, ?, ?
			);"""
		try:
			with sqlite3.connect(self.db) as conn:
				conn.execute(sql, (
					record.dbtime, record.name, record.levelno, record.levelname, record.msg, 
					str(record.args), record.module, record.funcName, record.lineno, record.exc_text, 
					record.process, record.thread, record.threadName, record.timestamp))
				conn.commit()  # not efficient, but hopefully thread-safe
		except Exception as e:
			print("Error in logging:", e)