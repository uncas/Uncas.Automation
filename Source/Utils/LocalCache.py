def getDb():
	import sqlite3
	return sqlite3.connect("Output/LocalCache.db")

def getOrAdd(key, getValue):
	db = getDb()
	db.execute("CREATE TABLE IF NOT EXISTS Cache (key TEXT PRIMARY KEY, value TEXT)")
	existingValue = db.execute("SELECT value FROM Cache WHERE key = ?", (key,)).fetchone()
	if existingValue:
		return existingValue
	
	value = getValue()
	db.execute("INSERT OR REPLACE INTO Cache (key, value) VALUES (?, ?)", (key, value))
	db.commit()
	return value

def getOrAddWithLifetime(key, getValue, lifetimeSeconds):
	import time
	db = getDb()
	db.execute("CREATE TABLE IF NOT EXISTS CacheWithLifetime (Key TEXT PRIMARY KEY, Value TEXT, ExpiryTimestamp INTEGER)")
	existingValue = db.execute("SELECT Value, ExpiryTimestamp FROM CacheWithLifetime WHERE Key = ?", (key,)).fetchone()
	nowTimestamp = time.time()
	if existingValue:
		expiryTimestamp = existingValue[1]
		if nowTimestamp <= expiryTimestamp:
			return existingValue[0]
	
	value = getValue()
	expiryTimestamp = nowTimestamp + lifetimeSeconds
	db.execute(
		"INSERT OR REPLACE INTO CacheWithLifetime (Key, Value, ExpiryTimestamp) VALUES (?, ?, ?)",
		(key, value, expiryTimestamp))
	db.commit()
	return value


def test_getOrAdd():
	import uuid
	key = "test-" + str(uuid.uuid4())
	class mock:
		def __init__(self):
			self.wasCalled = False
		def getValue(self):
			self.wasCalled = True
			return "42"
	
	myMock = mock()
	value = getOrAdd(key, myMock.getValue)
	print("Should be 42:", value)
	print("Was called should be True:", myMock.wasCalled)
	myMock = mock()
	value = getOrAdd(key, myMock.getValue)
	print("Should be 42:", value)
	print("Was called should be False:", myMock.wasCalled)

def test_getOrAddWithLifetime():
	import time
	import uuid
	key = "test-" + str(uuid.uuid4())
	value = getOrAddWithLifetime(key, lambda: "1", 0.5)
	print("Should be 1:", value)
	value = getOrAddWithLifetime(key, lambda: "2", 0.5)
	print("Should be 1:", value)
	time.sleep(1)
	value = getOrAddWithLifetime(key, lambda: "2", 0.5)
	print("Should be 2:", value)
