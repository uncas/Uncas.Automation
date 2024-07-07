def getOrAdd(key, getValue):
	import sqlite3
	db = sqlite3.connect("Output/LocalCache.db")
	db.execute("CREATE TABLE IF NOT EXISTS Cache (key TEXT PRIMARY KEY, value TEXT)")
	existingValue = db.execute("SELECT value FROM Cache WHERE key = ?", (key,)).fetchone()
	if existingValue:
		return existingValue
	
	value = getValue()
	db.execute("INSERT OR REPLACE INTO Cache VALUES (?, ?)", (key, value))
	db.commit()
	return value
