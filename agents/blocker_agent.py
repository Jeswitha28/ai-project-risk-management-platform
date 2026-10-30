from agents.retriever import gather_context
from agents.llm import ask_llm_json

SEARCHES = [
    "action items to do assigned to owner",
    "pending decision to be decided approval needed",
    "unresolved issue blocker blocked stuck",
    "next steps follow up by date",
    "meeting notes discussion progress update",
]

PROMPT = """You are an assistant that reads meeting notes and progress updates.
Use ONLY the text below. Do not invent owners or dates.
If an owner or due date is missing, use the words "Not mentioned".
If the same task appears more than once, list it only once and keep the most detailed evidence.
For every evidence field, also add a "source_file" field with the file name shown in the [From: ...] line above that text.
Return ONLY valid JSON in exactly this shape:
{
  "pending_decisions": [{"decision": "...", "evidence": "sentence from the text","source_file": "..."}],
  "unresolved_issues": [{"issue": "...", "evidence": "sentence from the text","source_file": "..."}],
  "blockers": [{"blocker": "...", "blocking_what": "...", "evidence": "sentence from the text","source_file": "..."}],
  "action_items": [{"task": "...", "owner": "...", "due_date": "...", "status": "...", "evidence": "sentence from the text","source_file": "..."}]
}

DOCUMENT TEXT:
{context}
"""


def run():
    context = gather_context(SEARCHES)
    return ask_llm_json(PROMPT.replace("{context}", context))