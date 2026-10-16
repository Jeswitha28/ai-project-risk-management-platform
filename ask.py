from rag.vector_store import VectorStore

store = VectorStore()
print("Ask questions about your documents. Type 'exit' to stop.\n")

while True:
    question = input("Question: ").strip()
    if question.lower() in ("exit", "quit", ""):
        break

    hits = store.search(question, top_k=3)
    if not hits:
        print("Nothing indexed yet. Run build_index.py first.\n")
        continue

    for i, hit in enumerate(hits, 1):
        print(f"\n[{i}] {hit['filename']} (chunk {hit['chunk_index']}, score {hit['score']})")
        print(hit["text"])
    print("\n" + "-" * 60 + "\n")