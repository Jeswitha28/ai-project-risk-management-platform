from pathlib import Path
from models import Document


def parse_txt(file_path):
    path = Path(file_path)

    try:
        raw = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raw = path.read_text(encoding="latin-1")

    lines = [line.strip() for line in raw.splitlines()]
    text = "\n".join(line for line in lines if line)

    if not text:
        raise ValueError(f"{path.name} is empty.")

    return Document(
        filename=path.name,
        file_type="txt",
        text=text,
    )