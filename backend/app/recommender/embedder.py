"""Article embedding using sentence-transformers (all-MiniLM-L6-v2)."""

from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

_model = SentenceTransformer(MODEL_NAME)


class Embedder:
    """Generates dense vector embeddings for articles using a local model."""

    def embed_text(self, text: str) -> list[float]:
        """Return a 384-dim embedding vector for the given text."""
        return _model.encode(text, normalize_embeddings=True).tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Batch-embed a list of texts. Returns list of 384-dim vectors."""
        return _model.encode(texts, batch_size=32, normalize_embeddings=True).tolist()


embedder = Embedder()