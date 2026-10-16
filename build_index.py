from pathlib import Path
from ingestion.loader import load_document
from rag.chunker import chunk_document
from rag.vector_store import VectorStore

CHUNK_SIZE = 300
OVERLAP = 50

store = VectorStore()

for file in sorted(Path("data/sample_docs").iterdir()):
    try:
        doc = load_document(file)
        chunks = chunk_document(doc, CHUNK_SIZE, OVERLAP)
        store.add_chunks(chunks)
        print(f"Indexed {doc.filename:30} -> {len(chunks)} chunks")
    except Exception as e:
        print(f"Skipped {file.name:30} -> {e}")

print("\nTotal chunks in store:", store.collection.count())