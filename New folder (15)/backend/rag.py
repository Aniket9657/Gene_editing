from langchain.vectorstores import FAISS
from langchain.embeddings import OllamaEmbeddings
from langchain.llms import Ollama
from langchain.document_loaders import TextLoader

# Load docs
loader = TextLoader("data/gondia.txt")
documents = loader.load()

# Embeddings
embedding = OllamaEmbeddings(model="llama3")

# Vector DB
db = FAISS.from_documents(documents, embedding)

# LLM
llm = Ollama(model="llama3")

def ask_rag(query):
    docs = db.similarity_search(query, k=3)
    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
    You are an intelligent AI assistant.
    Answer ONLY from the context below.

    Context:
    {context}

    Question:
    {query}
    """

    return llm(prompt)