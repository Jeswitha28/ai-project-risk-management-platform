from agents.retriever import gather_context

text = gather_context(["project goals", "deadline", "action items"])
print(text[:2000])