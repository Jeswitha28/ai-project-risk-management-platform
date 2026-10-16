from pathlib import Path
from ingestion.loader import load_document
from rag.chunker import chunk_document

for file in sorted(Path("data/sample_docs").iterdir()):
    doc = load_document(file)
    chunks = chunk_document(doc)
    print(f"{doc.filename:30} chars={len(doc.text):4}  chunks={len(chunks)}")

print("\n--- Stress test with a long text ---")
long_text = "\n".join(
    f"Sentence number {i} says that the project risk level is rising because of delay {i}."
    for i in range(1, 60)
)
from models import Document
big = Document(filename="long.txt", file_type="txt", text=long_text)
chunks = chunk_document(big)
print("Total chunks:", len(chunks))
print("Longest chunk:", max(len(c.text) for c in chunks), "chars")
print("\nEnd of chunk 0:\n", chunks[0].text[-120:])
print("\nStart of chunk 1:\n", chunks[1].text[:120])