# With langchain setup from https://python.langchain.com/v0.1/docs/integrations/vectorstores/chroma/

class EmbeddingVectorStore:
    def __init__(self, directory, logger):
        self.directory = directory
        self.logger = logger
    
    def getEmbeddingFunction(self):
        self.logger.debug("Importing sentence_transformer")
        from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings # type: ignore
        self.logger.debug("Creating embedding function")
        return SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    
    def save(self, textFile):
        from langchain_chroma import Chroma # type: ignore
        from langchain_community.document_loaders import TextLoader # type: ignore
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        # load the document
        loader = TextLoader(textFile)
        documents = loader.load()

        # split it into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)
        docs = text_splitter.split_documents(documents)

        # save to disk
        Chroma.from_documents(docs, self.getEmbeddingFunction(), persist_directory = self.directory)
    
    def load(self):
        from langchain_chroma import Chroma # type: ignore
        return Chroma(persist_directory = self.directory, embedding_function = self.getEmbeddingFunction())

    def getSimilarities(self, query):
        db = self.load()
        return db.similarity_search(query)

vectorStoreDirectory = "./chroma_db"

def getVectorStore(logger):
    return EmbeddingVectorStore(vectorStoreDirectory, logger).load()

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
    store = EmbeddingVectorStore(vectorStoreDirectory, logger)
    store.save(fileName)

if __name__ == "__main__":
	initialize()
