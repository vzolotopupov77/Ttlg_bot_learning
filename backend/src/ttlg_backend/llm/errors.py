"""LLM-specific errors."""


class LLMUnavailableError(Exception):
    """Raised when the LLM provider fails or times out."""
