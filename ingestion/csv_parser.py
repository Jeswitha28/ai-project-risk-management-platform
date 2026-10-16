from pathlib import Path
import pandas as pd
from models import Document


def parse_csv(file_path):
    path = Path(file_path)

    try:
        df = pd.read_csv(path)
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="latin-1")
    except pd.errors.EmptyDataError:
        raise ValueError(f"{path.name} is empty.")

    if df.empty:
        raise ValueError(f"No data rows found in {path.name}.")

    lines = []
    for _, row in df.iterrows():
        pairs = [f"{col}: {val}" for col, val in row.items() if pd.notna(val)]
        lines.append(" | ".join(pairs))

    return Document(
        filename=path.name,
        file_type="csv",
        text="\n".join(lines),
        page_count=len(df),
    )