from rag.vector_store import VectorStore

store = VectorStore()


def gather_context(search_questions, per_question=5):
    """Ask the library several questions, skip repeated pages,
    and glue all the pieces into one block of text."""
    seen = set()
    pieces = []
    for q in search_questions:
        hits = store.search(q, top_k=per_question)
        for hit in hits:
            key = (hit["filename"], hit["chunk_index"])
            if key in seen:
                continue
            seen.add(key)
            pieces.append(
                f"[From: {hit['filename']}, chunk {hit['chunk_index']}]\n{hit['text']}"
            )
    return "\n\n".join(pieces)