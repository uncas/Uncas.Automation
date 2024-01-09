import requests, json

chatUrl = "http://127.0.0.1:5000/v1/chat/completions"
completionsUrl = "http://127.0.0.1:5000/v1/completions"
headers = { "Content-Type": "application/json" }

def getCompletionResponse(prompt):
    data = {
        "prompt": prompt,
        "max_new_tokens": 250,
        "max_tokens": 250,
        "temperature": 0.5,
        "repetition_penalty": 1.1,
        "top_p": 0.9,
        "seed": 102,
        "stream": False,
        "stopping_strings": [ '\nUser:', '\n***' ],
        "stop": [ '\nUser:', '\n***' ],
        "skip_special_tokens": True
    }
    response = requests.post(completionsUrl, headers=headers, json=data, verify=False)
    responseJson = response.json()
    print(responseJson['model'])
    return responseJson

def getChatCompletionResponse(history):
    data = {
        "mode": "chat",
        "character": "Example",
        "messages": history
    }
    response = requests.post(chatUrl, headers=headers, json=data, verify=False)
    return response.json()

def getAndAppendChatCompletion(message, history):
    history.append({"role": "user", "content": message})
    responseContent = getChatCompletionResponse(history)
    assistant_message = responseContent['choices'][0]['message']['content']
    history.append({"role": "assistant", "content": assistant_message})
    return responseContent

def chat():
    history = []
    print("Welcome to the chat!")
    while True:
        user_message = input("> ")
        responseContent = getAndAppendChatCompletion(user_message, history)
        #print(json.dumps(responseContent, indent = 2))
        #model = responseContent['model']
        print(history[-1]['content'])

def completion():
    import datetime
    import time

    start = time.time()
    prompt = "What is the name of the president?"
    response = getCompletionResponse(prompt)
    print(response['choices'][0]['text'])
    llm = response['model']
    now = datetime.datetime.now().isoformat()
    parameters = "bla"

    end = time.time()
    durationMilliseconds = (end - start)*1000

    writeToLlmLog(llm, now, prompt, durationMilliseconds, response, parameters)

def writeToLlmLog(llm, date, prompt, durationMilliseconds, response, parameters):
    dbFile = "LlmLog.db"
    createTableSql = "CREATE TABLE IF NOT EXISTS LlmLog (Id integer PRIMARY KEY, Llm text NOT NULL, Date text NOT NULL, Prompt text NOT NULL, DurationMilliseconds integer NOT NULL, Response text NOT NULL, Parameters text NOT NULL);"
    try:
        conn = createConnection(dbFile)
        createTable(conn, createTableSql)
        insertLlmLog(conn, llm, date, prompt, durationMilliseconds, response, parameters)
    finally:
        if conn:
            conn.close()

def insertLlmLog(conn, llm, date, prompt, durationMilliseconds, response, parameters):
    """
    Insert Llm Log
    :param conn:
    :param llmLog:
    """
    sql = ''' INSERT INTO LlmLog(Llm, Date, Prompt, DurationMilliseconds, Response, Parameters)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    llmLog = (llm, date, prompt, durationMilliseconds, json.dumps(response), parameters)
    cur.execute(sql, llmLog)
    conn.commit()

def createConnection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    import sqlite3
    from sqlite3 import Error
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def createTable(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    from sqlite3 import Error
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

completion()
