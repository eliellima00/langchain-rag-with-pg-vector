import os 
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
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
        raise RuntimeError(f"Environment variable {k} is not set")

current_dir = Path(__file__).parent
root_dir = current_dir.parent
pdf_path =  os.getenv("PDF_PATH")

if not pdf_path:
    raise RuntimeError("PDF PATH cannot be null")

document_path = str(root_dir) + '/' + pdf_path

docs = PyPDFLoader(document_path).load()

chunks = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 150,
    add_start_index=False
).split_documents(docs) 

if not chunks:
    raise SystemExit(0)


enriched = []
for d in chunks:
    meta = {k: v for k, v in d.metadata.items() if k not in ("", None)}
    new_doc = Document(
        page_content=d.page_content,
        metadata=meta
    )
    enriched.append(new_doc)

ids = [f"doc-{i}" for i in range(len(enriched))]

embeddingsDocuments = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))

store = PGVector(
    embeddings=embeddingsDocuments,
    collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME", "rag-collection"),
    connection=os.getenv("DATABASE_URL"),
    use_jsonb=True
)

store.add_documents(documents=enriched, ids=ids)
print("EMBEDDING FINISHED WITH SUCCESS")
