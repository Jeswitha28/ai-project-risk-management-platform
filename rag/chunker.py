import re
from models import Chunk


def _split_units(text, max_len):
    units = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        if len(line) <= max_len:
            units.append(line)
            continue
        for sentence in re.split(r"(?<=[.!?])\s+", line):
            if len(sentence) <= max_len:
                units.append(sentence)
            else:
                for i in range(0, len(sentence), max_len):
                    units.append(sentence[i:i + max_len])
    return units


def chunk_text(text, chunk_size=600, overlap=100):
    units = _split_units(text, chunk_size)
    chunks = []
    current = []
    current_len = 0

    for unit in units:
        extra = len(unit) + (1 if current else 0)

        if current and current_len + extra > chunk_size:
            chunks.append("\n".join(current))

            keep = []
            keep_len = 0
            for u in reversed(current):
                add = len(u) + (1 if keep else 0)
                if keep_len + add > overlap:
                    break
                keep.insert(0, u)
                keep_len += add

            while keep and keep_len + 1 + len(unit) > chunk_size:
                removed = keep.pop(0)
                keep_len -= len(removed) + (1 if keep else 0)

            current = keep
            current_len = keep_len
            extra = len(unit) + (1 if current else 0)

        current.append(unit)
        current_len += extra

    if current:
        chunks.append("\n".join(current))

    return chunks


def chunk_document(doc, chunk_size=600, overlap=100):
    pieces = chunk_text(doc.text, chunk_size, overlap)
    return [
        Chunk(
            text=piece,
            doc_id=doc.doc_id,
            filename=doc.filename,
            file_type=doc.file_type,
            chunk_index=i,
            project_id=doc.project_id,
        )
        for i, piece in enumerate(pieces)
    ]