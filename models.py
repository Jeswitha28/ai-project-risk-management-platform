from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Document:
    filename: str
    file_type: str
    text: str
    page_count: int = 0
    project_id: str = "default"
    doc_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    uploaded_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Chunk:
    text: str
    doc_id: str
    filename: str
    file_type: str
    chunk_index: int
    project_id: str = "default"
    chunk_id: str = ""

    def __post_init__(self):
        if not self.chunk_id:
            self.chunk_id = f"{self.doc_id}_{self.chunk_index}"