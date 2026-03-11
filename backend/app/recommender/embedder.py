"""Article embedding using sentence-transformers (all-MiniLM-L6-v2)."""

# TODO: from sentence_transformers import SentenceTransformer
# TODO: Load model once at module level (singleton pattern to avoid re-load)
# MODEL_NAME = "all-MiniLM-L6-v2"


class Embedder:
    """Generates dense vector embeddings for articles using a local model."""

    def __init__(self):
        # TODO: self.model = SentenceTransformer(MODEL_NAME)
        pass

    def embed_text(self, text: str) -> list[float]:
        """
        Return a 384-dim embedding vector for the given text.
        Input text should be a concatenation of title + description.
        """
        # TODO: return self.model.encode(text).tolist()
        raise NotImplementedError

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Batch-embed a list of texts. More efficient than calling embed_text in a loop.
        Returns a list of embedding vectors.
        """
        # TODO: return self.model.encode(texts, batch_size=32).tolist()
        raise NotImplementedError
