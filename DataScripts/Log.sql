SELECT
	Created, 
	LogLevelName, 
	LogLevel,
	Message, 
	Args,
	Exception
	, Source, Module, FuncName, LineNo
FROM log
--WHERE LogLevel > 20
ORDER BY TimeStamp DESC
LIMIT 10