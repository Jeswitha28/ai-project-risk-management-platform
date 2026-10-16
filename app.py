import re
from pathlib import Path

import streamlit as st

from ingestion.loader import load_document
from rag.chunker import chunk_document
from rag.vector_store import VectorStore

PROJECT_TITLE = "Development of AI-Driven Enterprise Project Intelligence & Risk Management Platform"
UPLOAD_DIR = Path("data/uploads")
SUPPORTED_TYPES = ["pdf", "docx", "csv", "txt"]

MODULES = [
    {"Module": "Document Ingestion (PDF, DOCX, CSV, TXT)", "Status": "Milestone 1 - Done"},
    {"Module": "RAG Pipeline (chunking, embedding, vector index)", "Status": "Milestone 1 - Done"},
    {"Module": "Scope and Deliverable Extraction Agent", "Status": "Planned"},
    {"Module": "Risk Detection and Delivery Forecasting Agent", "Status": "Planned"},
    {"Module": "Blocker and Action Item Identification Agent", "Status": "Planned"},
    {"Module": "Documentation Generation Agent", "Status": "Planned"},
    {"Module": "Project Health Scoring Module", "Status": "Planned"},
    {"Module": "Conversational Project Intelligence Assistant", "Status": "Planned"},
    {"Module": "Project Insights and Risk Summary Dashboard", "Status": "Planned"},
]

st.set_page_config(page_title="Enterprise Project Intelligence Platform", layout="wide")


@st.cache_resource
def get_store():
    return VectorStore()


def clean_project_id(name):
    cleaned = re.sub(r"[^a-z0-9_-]+", "-", name.strip().lower()).strip("-")
    return cleaned or "default"


def index_file(uploaded_file, project_id, store, chunk_size, overlap):
    folder = UPLOAD_DIR / project_id
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / Path(uploaded_file.name).name
    path.write_bytes(uploaded_file.getbuffer())

    doc = load_document(path)
    doc.project_id = project_id
    chunks = chunk_document(doc, chunk_size, overlap)
    store.add_chunks(chunks)
    return doc, len(chunks)


store = get_store()

st.title(PROJECT_TITLE)
st.caption("Milestone 1: document ingestion and RAG knowledge base")

with st.sidebar:
    st.header("Project")
    project_name = st.text_input("Project name", value="default")
    project_id = clean_project_id(project_name)
    st.write(f"Project ID: `{project_id}`")

    st.header("Chunk settings")
    chunk_size = st.slider("Chunk size (characters)", 200, 1000, 600, 50)
    overlap = st.slider("Overlap (characters)", 0, 200, 100, 10)

tab_upload, tab_ask, tab_roadmap = st.tabs(
    ["1. Upload documents", "2. Ask questions", "3. Platform roadmap"]
)

with tab_upload:
    files = st.file_uploader(
        "Upload project documents (PDF, DOCX, CSV, TXT). You can select several files at once.",
        type=SUPPORTED_TYPES,
        accept_multiple_files=True,
    )

    if st.button("Index documents", type="primary", disabled=not files):
        progress = st.progress(0)
        succeeded = 0
        failed = 0
        for i, f in enumerate(files, 1):
            try:
                with st.spinner(f"Indexing {f.name}..."):
                    doc, n_chunks = index_file(f, project_id, store, chunk_size, overlap)
                st.success(f"{doc.filename}: {len(doc.text)} characters, {n_chunks} chunks indexed")
                succeeded += 1
            except Exception as e:
                st.error(f"{f.name}: {e}")
                failed += 1
            progress.progress(i / len(files))
        st.info(f"Done: {succeeded} indexed, {failed} failed, out of {len(files)} files.")

with tab_ask:
    question = st.text_input("Ask a question about your project documents")
    top_k = st.slider("Number of results", 1, 10, 3)

    if question:
        hits = store.search(question, project_id=project_id, top_k=top_k)
        if not hits:
            st.warning("Nothing indexed for this project yet. Upload documents first.")
        for i, hit in enumerate(hits, 1):
            title = f"[{i}] {hit['filename']} - chunk {hit['chunk_index']} - score {hit['score']}"
            with st.expander(title, expanded=(i == 1)):
                st.text(hit["text"])

with tab_roadmap:
    st.write("Modules of the platform and their status.")
    st.table(MODULES)