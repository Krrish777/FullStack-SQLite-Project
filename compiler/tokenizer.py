import re
from utils.errors import TokenizationError
from utils.logger import get_logger
from compiler.token_definitions import TOKEN_PATTERN

logger = get_logger(__name__)

class Tokenizer:
    def __init__(self):
        self.patterns = [(typ, re.compile(pat, re.IGNORECASE)) for typ, pat in TOKEN_PATTERN]

    def tokenize(self, sql):
        logger.info("Starting tokenization process.")
        tokens = []
        position = 0
        sql = sql.strip()

        while position < len(sql):
            if sql[position].isspace():
                position += 1
                continue

            if sql[position:position + 2] == "--":
                end = sql.find("\n", position)
                position = end + 1 if end != -1 else len(sql)
                continue

            match_found = False
            for token_type, pattern in self.patterns:
                match = pattern.match(sql, position)
                
                if match:
                    value = match.group(0)
                    token_value = value.upper() if token_type == "KEYWORD" else value
                    tokens.append((token_type, token_value))
                    logger.debug(f"Tokenized: {token_type} -> {token_value}")
                    position = match.end()
                    match_found = True
                    break

            if not match_found:
                raise TokenizationError(f"Unexpected character: {sql[position]} at position {position}")

        tokens.append(("EOF", None))
        logger.info("Tokenization complete.")
        return tokens