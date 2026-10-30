import os
import json
import time
from dotenv import load_dotenv

load_dotenv()  # reads your secret .env file

PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()


def _ask_once(prompt):
    """Send a question to the AI one time."""
    if PROVIDER == "gemini":
        from google import genai
        client = genai.Client()  # finds GEMINI_API_KEY by itself
        model = os.getenv("LLM_MODEL", "gemini-3.8-flash")
        reply = client.models.generate_content(model=model, contents=prompt)
        return reply.text

    if PROVIDER == "claude":
        from anthropic import Anthropic
        client = Anthropic()  # finds ANTHROPIC_API_KEY by itself
        model = os.getenv("LLM_MODEL", "claude-sonnet-5-5")
        reply = client.messages.create(
            model=model,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )
        return reply.content[0].text

    if PROVIDER == "groq":
        from groq import Groq
        client = Groq()  # finds GROQ_API_KEY by itself
        model = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
        reply = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        return reply.choices[0].message.content

    raise ValueError(f"Unknown LLM_PROVIDER: {PROVIDER}")


def ask_llm(prompt, tries=5):
    """Ask the AI. If the server is busy, wait and try again."""
    wait = 5
    for attempt in range(1, tries + 1):
        try:
            return _ask_once(prompt)
        except Exception as error:
            message = str(error)
            busy = "503" in message or "429" in message or "UNAVAILABLE" in message
            if busy and attempt < tries:
                print(f"Server busy. Waiting {wait} seconds, then trying again ({attempt}/{tries})...")
                time.sleep(wait)
                wait *= 2   # wait longer each time: 5, 10, 20, 40
            else:
                raise


def ask_llm_json(prompt):
    """Ask the AI and turn its answer into a Python dictionary."""
    text = ask_llm(prompt)
    start, end = text.find("{"), text.rfind("}")   # keep only the { ... } part
    if start == -1 or end == -1:
        return {"error": "AI did not return JSON", "raw": text}
    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        return {"error": "JSON was broken", "raw": text}