import chromadb
from rag.embedder import embed_texts, embed_query


class VectorStore:
    def __init__(self, path="chroma_db"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(
            name="project_chunks",
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(self, chunks):
        if not chunks:
            return 0

        first = chunks[0]
        self.collection.delete(
            where={
                "$and": [
                    {"filename": first.filename},
                    {"project_id": first.project_id},
                ]
            }
        )

        self.collection.add(
            ids=[c.chunk_id for c in chunks],
            documents=[c.text for c in chunks],
            embeddings=embed_texts([c.text for c in chunks]),
            metadatas=[
                {
                    "project_id": c.project_id,
                    "doc_id": c.doc_id,
                    "filename": c.filename,
                    "file_type": c.file_type,
                    "chunk_index": c.chunk_index,
                }
                for c in chunks
            ],
        )
        return len(chunks)

    def search(self, question, project_id="default", top_k=3):
        in_project = len(
            self.collection.get(where={"project_id": project_id}, include=[])["ids"]
        )
        if in_project == 0:
            return []

        result = self.collection.query(
            query_embeddings=[embed_query(question)],
            n_results=min(top_k, in_project),
            where={"project_id": project_id},
        )

        hits = []
        for text, meta, dist in zip(
            result["documents"][0], result["metadatas"][0], result["distances"][0]
        ):
            hits.append(
                {
                    "text": text,
                    "filename": meta["filename"],
                    "chunk_index": meta["chunk_index"],
                    "score": round(1 - dist, 3),
                }
            )
        return hits

    def list_documents(self, project_id="default"):
        data = self.collection.get(
            where={"project_id": project_id}, include=["metadatas"]
        )
        counts = {}
        for meta in data["metadatas"]:
            key = (meta["filename"], meta["file_type"])
            counts[key] = counts.get(key, 0) + 1
        return [
            {"File": name, "Type": ftype, "Chunks": n}
            for (name, ftype), n in sorted(counts.items())
        ]