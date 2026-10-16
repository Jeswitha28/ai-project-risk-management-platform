from pathlib import Path
from pypdf import PdfReader
from models import Document


def parse_pdf(file_path):
    path = Path(file_path)
    reader = PdfReader(path)

    pages = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text.strip())

    full_text = "\n\n".join(p for p in pages if p)

    if not full_text:
        raise ValueError(
            f"No extractable text in {path.name}. It may be a scanned PDF."
        )

    return Document(
        filename=path.name,
        file_type="pdf",
        text=full_text,
        page_count=len(reader.pages),
    )
