# With langchain setup from https://python.langchain.com/v0.1/docs/integrations/vectorstores/chroma/

class EmbeddingVectorStore:
    def __init__(self, directory):
        import logging
        self.directory = directory
        self.textSplitter = None
        self.embeddingFunction = None
        self.logger = logging.getLogger(__name__)
    
    def getEmbeddingFunction(self):
        if not self.embeddingFunction:
            self.logger.debug("Importing sentence_transformer")
            from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings # type: ignore
            self.logger.debug("Creating embedding function")
            self.embeddingFunction = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        return self.embeddingFunction

    def getTextSplitter(self):
        if not self.textSplitter:
            from langchain_text_splitters import RecursiveCharacterTextSplitter
            self.textSplitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)
        return self.textSplitter

    def save(self, textFile):
        from langchain_chroma import Chroma # type: ignore
        from langchain_community.document_loaders import TextLoader # type: ignore
        loader = TextLoader(textFile)
        documents = loader.load()
        docs = self.getTextSplitter().split_documents(documents)
        Chroma.from_documents(docs, self.getEmbeddingFunction(), persist_directory = self.directory)
    
    def load(self):
        from langchain_chroma import Chroma # type: ignore
        return Chroma(persist_directory = self.directory, embedding_function = self.getEmbeddingFunction())

    def get_similarities(self, query):
        db = self.load()
        return db.similarity_search(query)
