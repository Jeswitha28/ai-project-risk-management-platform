# Development of AI-Driven Enterprise Project Intelligence & Risk Management Platform

Milestone 1: document ingestion, RAG pipeline and upload interface.

## What is built
- Upload PDF, DOCX, CSV and TXT files (several at once)
- Split the text into chunks, convert them into embeddings, store them in ChromaDB
- Ask questions and see the best matching chunks with source and score

## Setup
pip install -r requirements.txt

## Run
streamlit run app.py

## Milestone 2: Multi-Agent Analysis

Three agents analyse the uploaded project documents. Each agent retrieves
relevant chunks from ChromaDB, asks an LLM to answer in JSON, and attaches
an evidence sentence and source file to every finding.

| Agent | File | What it finds |
|---|---|---|
| Scope & Deliverable Extraction | agents/scope_agent.py | Goals, deliverables, milestones, timeline, responsibilities |
| Risk Detection & Delivery Forecasting | agents/risk_agent.py | Schedule risks, dependency gaps, delivery challenges, forecast |
| Blocker & Action Item Identification | agents/blocker_agent.py | Pending decisions, unresolved issues, blockers, action items |

### How to run
1. Put documents (PDF, DOCX, TXT, CSV) in `data/` and run `python build_index.py`
2. Create a `.env` file with `LLM_PROVIDER`, `GEMINI_API_KEY` and `LLM_MODEL`
3. Run `python run_agents.py`. Results are saved to `outputs/results.json`

### Design choices
- Agents answer only from the documents, and write "Not mentioned" when a detail is missing
- Every finding includes an evidence sentence and its source file
- `llm.py` retries automatically when the AI server is busy
- The LLM provider can be switched (Gemini, Claude, Groq) through `.env`

### Validation
Tested on documents in PDF, DOCX, TXT and CSV formats. See the validation table.

### Known limitations
- Overdue tasks are not flagged automatically
- Conflicting numbers in different documents are not reconciled