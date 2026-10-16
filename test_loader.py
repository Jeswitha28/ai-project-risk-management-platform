from pathlib import Path
from ingestion.loader import load_document

folder = Path("data/sample_docs")

for file in sorted(folder.iterdir()):
    try:
        doc = load_document(file)
        print(f"OK     {doc.filename:30} type={doc.file_type:5} chars={len(doc.text)}")
    except Exception as e:
        print(f"FAILED {file.name:30} -> {e}")