from agents.retriever import gather_context
from agents.llm import ask_llm_json

SEARCHES = [
    "project goals and objectives",
    "project scope and deliverables",
    "milestones and phases",
    "timeline schedule start date end date deadline",
    "team members roles and responsibilities",
]

PROMPT = """You are a project analyst. Read ONLY the document text below.
Do not use outside knowledge and do not guess.
If something is not in the text, write "Not mentioned".
For every evidence field, also add a "source_file" field with the file name shown in the [From: ...] line above that text.
Return ONLY valid JSON in exactly this shape:
{{
  "goals": ["..."],
  "deliverables": ["..."],
  "milestones": [{{"name": "...", "date": "...", "evidence": "short sentence copied from the text","source_file": "..."}}],
  "timeline": {{"start": "...", "end": "..."}},
  "responsibilities": [{{"person": "...", "task": "...", "evidence": "...","source_file": "..."}}]

}}

DOCUMENT TEXT:
{context}
"""

def run():
    context = gather_context(SEARCHES)
    return ask_llm_json(PROMPT.format(context=context))