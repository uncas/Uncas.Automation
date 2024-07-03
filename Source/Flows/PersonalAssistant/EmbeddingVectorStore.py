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
