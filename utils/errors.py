class TokenizationError(Exception):
    """Raised when an unknown token is encountered during tokenization."""
    pass
class ParserError(Exception):
    """Raised when an error occurs during parsing."""
    pass