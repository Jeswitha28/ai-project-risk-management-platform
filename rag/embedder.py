from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
_model = None


def get_model():
    global _model
    if _model is None:
        print("Loading embedding model (first run downloads it)...")
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def embed_texts(texts):
    vectors = get_model().encode(texts, normalize_embeddings=True)
    return vectors.tolist()


def embed_query(question):
    return embed_texts([question])[0]