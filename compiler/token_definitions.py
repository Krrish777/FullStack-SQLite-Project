TOKEN_PATTERN = [
    ("KEYWORD", r"\b(SELECT|FROM|INSERT|INTO|VALUES|CREATE|TABLE|WHERE|AND|OR|UPDATE|SET|DELETE|JOIN|ORDER|BY|GROUP)\b"),
    ("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("NUMBER", r"\b\d+(\.\d+)?\b"),
    ("STRING", r"'[^']*'"),
    ("COMMA", r","),
    ("SEMICOLON", r";"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("OPERATOR", r"[+\-*/=<>]"),
    ("ASTERISK", r"\*")
]