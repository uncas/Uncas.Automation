class LocalCache:
	def __init__(self, cacheDbName = "LocalCache"):
		import sqlite3
		self.db = sqlite3.connect("Output/" + cacheDbName + ".db")

	def getOrAdd(self, key, getValue):
		self.db.execute("CREATE TABLE IF NOT EXISTS Cache (key TEXT PRIMARY KEY, value TEXT)")
		existingValue = self.db.execute("SELECT value FROM Cache WHERE key = ?", (key,)).fetchone()
		if existingValue:
			return existingValue
		
		value = getValue()
		self.db.execute("INSERT OR REPLACE INTO Cache (key, value) VALUES (?, ?)", (key, value))
		self.db.commit()
		return value
	
	def getOrAddWithLifetime(self, key, getValue, lifetimeSeconds):
		import time
		nowTimestamp = time.time()
		mustBeCreatedAfterTimestamp = nowTimestamp - lifetimeSeconds
		self.db.execute("CREATE TABLE IF NOT EXISTS CacheWithLifetime (Key TEXT PRIMARY KEY, Value TEXT, Timestamp INTEGER)")
		existingValue = self.db.execute("SELECT Value FROM CacheWithLifetime WHERE Key = ? AND Timestamp > ?", (key,mustBeCreatedAfterTimestamp,)).fetchone()
		if existingValue:
			return existingValue[0]
		
		value = getValue()
		self.db.execute(
			"INSERT OR REPLACE INTO CacheWithLifetime (Key, Value, Timestamp) VALUES (?, ?, ?)",
			(key, value, nowTimestamp))
		self.db.commit()
		return value

def test_getOrAdd():
	import uuid
	cache = LocalCache("LocalCacheTest")
	key = "test-" + str(uuid.uuid4())
	class mock:
		def __init__(self):
			self.wasCalled = False
		def getValue(self):
			self.wasCalled = True
			return "42"
	
	myMock = mock()
	value = cache.getOrAdd(key, myMock.getValue)
	print("Should be 42:", value)
	print("Was called should be True:", myMock.wasCalled)
	myMock = mock()
	value = cache.getOrAdd(key, myMock.getValue)
	print("Should be 42:", value)
	print("Was called should be False:", myMock.wasCalled)

def test_getOrAddWithLifetime():
	import time
	import uuid
	cache = LocalCache("LocalCacheTest")
	key = "test-" + str(uuid.uuid4())
	value = cache.getOrAddWithLifetime(key, lambda: "1", 0.5)
	print("Should be 1:", value)
	value = cache.getOrAddWithLifetime(key, lambda: "2", 0.5)
	print("Should be 1:", value)
	time.sleep(1)
	value = cache.getOrAddWithLifetime(key, lambda: "2", 0.5)
	print("Should be 2:", value)
