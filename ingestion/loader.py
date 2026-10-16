from pathlib import Path
from ingestion.pdf_parser import parse_pdf
from ingestion.docx_parser import parse_docx
from ingestion.csv_parser import parse_csv
from ingestion.txt_parser import parse_txt

PARSERS = {
    ".pdf": parse_pdf,
    ".docx": parse_docx,
    ".csv": parse_csv,
    ".txt": parse_txt,
}


def load_document(file_path):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    extension = path.suffix.lower()
    parser = PARSERS.get(extension)

    if parser is None:
        supported = ", ".join(PARSERS)
        raise ValueError(f"Unsupported file type '{extension}'. Supported: {supported}")

    return parser(path)