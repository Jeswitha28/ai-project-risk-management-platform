from agents.retriever import gather_context
from agents.llm import ask_llm_json

SEARCHES = [
    "delay delayed behind schedule postponed slipped",
    "risk concern challenge",
    "dependency depends on waiting for client approval",
    "deadline at risk resource shortage on leave",
    "blocked cannot start until",
]

PROMPT = """You are a project risk analyst. Read ONLY the document text below.
Every risk must be backed by something written in the text.
If the text gives no support for a risk, do NOT include it.
If something is not written in the text, use the words "Not mentioned".
For every evidence field, also add a "source_file" field with the file name shown in the [From: ...] line above that text.
Return ONLY valid JSON in exactly this shape:
{
  "schedule_risks": [{"risk": "...", "severity": "High/Medium/Low", "evidence": "sentence from the text", "why_it_matters": "...","source_file": "..."}],
  "dependency_gaps": [{"gap": "...", "evidence": "sentence from the text","source_file": "..."}],
  "delivery_challenges": [{"challenge": "...", "evidence": "sentence from the text","source_file": "..."}],
  "delivery_forecast": {
    "status": "On track / At risk / Likely delayed",
    "reason": "one or two simple sentences based on the evidence above"
  }
}

DOCUMENT TEXT:
{context}
"""


def run():
    context = gather_context(SEARCHES)
    return ask_llm_json(PROMPT.replace("{context}", context))