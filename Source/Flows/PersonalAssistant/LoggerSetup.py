def initLogger():
	import logging
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