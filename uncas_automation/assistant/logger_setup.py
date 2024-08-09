def init_logger():
	import logging
	from easai.utils.sqlite_logging_handler import SQLiteLoggingHandler
	from uncas_automation.Utils.ColoredLoggingFormatter import ColoredLoggingFormatter

	# 1. Create root logger
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)

	# 2. Create handlers
	console_handler = logging.StreamHandler()
	file_handler = logging.FileHandler("Data/Log.log", "a")
	sqlite_handler = SQLiteLoggingHandler(db = "Data/Log.db")

	# 3. Set the handlers' levels
	console_handler.setLevel(logging.WARNING)
	file_handler.setLevel(logging.DEBUG)
	sqlite_handler.setLevel(logging.DEBUG)

	# 4. Create formatters and add them to handlers
	# Formats: https://stackoverflow.com/a/16759818
	#defaultFormat = "%(levelname)s:%(name)s:%(message)s"
	advancedFormat = "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
	console_handler.setFormatter(ColoredLoggingFormatter(advancedFormat))
	file_handler.setFormatter(logging.Formatter(advancedFormat))

	# 5. Add handlers to the logger
	logger.addHandler(console_handler)
	logger.addHandler(file_handler)
	logger.addHandler(sqlite_handler)
