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