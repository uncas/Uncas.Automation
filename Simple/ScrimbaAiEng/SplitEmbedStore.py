# From Scrimba course in AI Engineering
# With langchain setup from https://python.langchain.com/v0.1/docs/integrations/vectorstores/chroma/

persist_directory = "./chroma_db"

def getEmbeddingFunction():
    from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
    # create the open-source embedding function
    return SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

def splitEmbedAndStore():
    from langchain_chroma import Chroma
    from langchain_community.document_loaders import TextLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    # load the document
    loader = TextLoader("scrimba-info.txt")
    documents = loader.load()

    # split it into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    # save to disk
    Chroma.from_documents(docs, getEmbeddingFunction(), persist_directory=persist_directory)

def getVectorStore():
    from langchain_chroma import Chroma
    return Chroma(persist_directory=persist_directory, embedding_function=getEmbeddingFunction())

def getSimilarities(query):
    db = getVectorStore()
    docs = db.similarity_search(query)
    return docs

splitEmbedAndStore()
docs = getSimilarities("What are the technical requirements for running Scrimba? I only have a very old laptop which is not that powerful.")
print(docs[0].page_content)
