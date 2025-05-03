from tokenizer import Tokenizer

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        pass

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self):
        if self.pos < len(self.tokens):
            self.pos += 1
        return self.current_token()

    def peek(self, offset=1):
        index = self.pos + offset
        if index < len(self.tokens):
            return self.tokens[index]
        return None

    def expect(self, token_type, value=None):
        token = self.current_token()
        if token is None:
            raise SyntaxError("Unexpected end of input")
        if token.type != token_type or (value is not None and token.value != value):
            raise SyntaxError(f"Expected {token_type} but got {token.type}")
        self.advance()
        return token

    def match(self, token_type, value=None):
        token = self.current_token()
        if token and token.type == token_type and (value is None or token.value == value):
            self.advance()
            return True
        return False


if __name__ == "__main__":
    from tokenizer import Tokenizer
    
    query = "SELECT * FROM users WHERE age > 30;"
    tokenizer = Tokenizer(query)
    tokens = tokenizer.tokenize()

    parser = Parser(tokens)

    print("First token:", parser.current_token())
    parser.advance()
    print("After advance:", parser.current_token())
    print("Peek:", parser.peek())
    print("Match SELECT:", parser.match("KEYWORD", "SELECT"))
    print("Expect *:", parser.expect("OPERATOR", "*"))