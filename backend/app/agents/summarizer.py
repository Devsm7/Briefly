"""LLM-powered article summarization via Ollama (Mistral 7B)."""

# TODO: Import requests or httpx
# TODO: Import settings from app.core.config

# Ollama API endpoint: {OLLAMA_BASE_URL}/api/generate


class Summarizer:
    """Generates 3-5 bullet point summaries for articles using a local LLM."""

    def summarize_article(self, title: str, content: str) -> str:
        """
        Call the Ollama API to generate a 3-5 bullet point summary.
        Prompt structure:
            "Summarize the following article in 3-5 concise bullet points.
             Include the key facts. Article title: {title}. Content: {content}"
        Returns a newline-separated bullet string, e.g.:
            "• Central bank raises rates by 0.25%\n• Markets react negatively..."
        Handles connection errors gracefully (return empty string on failure).
        """
        # TODO: build prompt
        # TODO: POST to {OLLAMA_BASE_URL}/api/generate with model=OLLAMA_MODEL
        # TODO: parse streaming response; concatenate text chunks
        # TODO: fallback to OpenAI if OPENAI_API_KEY is set and Ollama fails
        raise NotImplementedError

    def summarize_batch(self, articles: list) -> list[str]:
        """
        Summarize a list of Article objects in sequence.
        Returns a list of summary strings in the same order.
        """
        # TODO: loop over articles; call summarize_article; collect results
        raise NotImplementedError
