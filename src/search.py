import os 
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

required_environment = [
    "OPENAI_API_KEY",
    "OPENAI_EMBEDDING_MODEL",
    "DATABASE_URL", 
    "PG_VECTOR_COLLECTION_NAME",
    "PDF_PATH"
]


for k in (required_environment):
    if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} it not set")
    

embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))

store = PGVector(
    embeddings,
    collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME", "rag-collection"),
    connection=os.getenv("DATABASE_URL"),
    use_jsonb=True
)

def search_similar_documents(query: str, k: int = 10):
    """Busca documentos similares no vector store"""
    results = store.similarity_search_with_score(query, k)
    return results

