def initLogger():
	import logging
	from easai.Utils.SQLiteLoggingHandler import SQLiteLoggingHandler
	from easai.Utils.ColoredLoggingFormatter import ColoredLoggingFormatter

	# 1. Create root logger
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)

	# 2. Create handlers
	consoleHandler = logging.StreamHandler()
	fileHandler = logging.FileHandler("Data/Log.log", "a")
	sqliteHandler = SQLiteLoggingHandler(db = "Data/Log.db")

	# 3. Set the handlers' levels
	consoleHandler.setLevel(logging.WARNING)
	fileHandler.setLevel(logging.DEBUG)
	sqliteHandler.setLevel(logging.DEBUG)

	# 4. Create formatters and add them to handlers
	# Formats: https://stackoverflow.com/a/16759818
	#defaultFormat = "%(levelname)s:%(name)s:%(message)s"
	advancedFormat = "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
	consoleHandler.setFormatter(ColoredLoggingFormatter(advancedFormat))
	fileHandler.setFormatter(logging.Formatter(advancedFormat))

	# 5. Add handlers to the logger
	logger.addHandler(consoleHandler)
	logger.addHandler(fileHandler)
	logger.addHandler(sqliteHandler)
