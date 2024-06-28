# With langchain setup from https://python.langchain.com/v0.1/docs/integrations/vectorstores/chroma/

vectorStoreDirectory = "./chroma_db"

def getEmbeddingFunction(logger):
    logger.debug("Before importing sentence_transformer")
    from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings # type: ignore
    logger.debug("After importing sentence_transformer")
    # create the open-source embedding function
    result = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    logger.debug("After creating embedding function")
    return result

def splitEmbedAndStore(textFile, logger):
    from langchain_chroma import Chroma # type: ignore
    from langchain_community.document_loaders import TextLoader # type: ignore
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    # load the document
    loader = TextLoader(textFile)
    documents = loader.load()

    # split it into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    # save to disk
    Chroma.from_documents(docs, getEmbeddingFunction(logger), persist_directory=vectorStoreDirectory)

def getVectorStore(logger):
    from langchain_chroma import Chroma # type: ignore
    return Chroma(persist_directory=vectorStoreDirectory, embedding_function=getEmbeddingFunction(logger))

def getSimilarities(query, logger):
    db = getVectorStore(logger)
    docs = db.similarity_search(query)
    return docs

def initialize():
    from GoogleCalendarService import readNextEvents
    calendarFileContent = ""
    events = readNextEvents(100)
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        calendarFileContent += "Event: " + event["summary"] + "\n"
        calendarFileContent += "Start time: " + start + "\n"
        calendarFileContent += "Event type: " + event["eventType"] + "\n"
        calendarFileContent += "Status: " + event["status"] + "\n"
        if "description" in event:
            calendarFileContent += "Description: " + event["description"] + "\n"
        if "attendees" in event:
            attendeesEmails = ", ".join([attendee["email"] for attendee in event["attendees"]])
            calendarFileContent += "Attendees: " + attendeesEmails + "\n"
        calendarFileContent += "\n\n"
    import os
    folderName = "Output"
    if not os.path.exists(folderName):
        os.makedirs(folderName)
    fileName = folderName + "/calendar.txt"
    with open(fileName, "w") as f:
        f.write(calendarFileContent)
    from Logger import Logger
    logger = Logger()
    splitEmbedAndStore(fileName, logger)

if __name__ == "__main__":
	initialize()
