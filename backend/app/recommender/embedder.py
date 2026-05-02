"""Article embedding using sentence-transformers (all-MiniLM-L6-v2)."""

MODEL_NAME = "all-MiniLM-L6-v2"
from sentence_transformers import SentenceTransformer

_model = SentenceTransformer(MODEL_NAME)

class Embedder:
    """Generates dense vector embeddings for articles using a local model."""


    def embed_text(self, text: str) -> list[float]:
        """
        Return a 384-dim embedding vector for the given text.
        Input text should be a concatenation of title + description.
        FOR THE NEW NEWS ADDED
        """
        return _model.encode(text, normalize_embeddings=True).tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """
         FOR THE EXISTING news in the DB
        """
        return _model.encode(texts, batch_size=32 , normalize_embeddings=True).tolist()

embedder = Embedder()