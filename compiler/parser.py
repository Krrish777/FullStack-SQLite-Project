from utils.logger import get_logger

logger = get_logger(__name__)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            logger.debug(f"Current token: {token}")
            return token
        logger.debug("No current token, end of input reached.")
        return None

    def advance(self):
        if self.pos < len(self.tokens):
            logger.debug(f"Advancing from token: {self.tokens[self.pos]}")
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
            logger.error("Unexpected end of input")
            raise SyntaxError("Unexpected end of input")
        
        token_type_in_token, token_value_in_token = token
        
        if token_type_in_token != token_type or (value is not None and token_value_in_token != value):
            logger.error(f"Expected {token_type} but got {token_type_in_token}")
            raise SyntaxError(f"Expected {token_type} but got {token_type_in_token}")
        logger.debug(f"Expect matched at pos {self.pos}: {token}")
        self.advance()
        return token

    def match(self, token_type, value=None):
        token = self.current_token()
        if token:
            token_type_in_token, token_value_in_token = token
            if token_type_in_token == token_type and (value is None or token_value_in_token == value):
                logger.debug(f"Token successfully matched at pos {self.pos}: {token}")
                self.advance()
                return True
        logger.debug(f"Token match failed at pos {self.pos}: expected {token_type} but got {token}")
        return False
    
    def parse_select_list(self):
        logger.info("Parsing SELECT list")
        select_list = []
        while True:
            token = self.current_token()
            if token is None:
                logger.error("End of token stream while parsing SELECT list")
                break
            token_type, token_value = token

            if token_type == "ASTERISK":
                select_list.append("*")
                logger.debug("Added '*' to SELECT list")
                self.advance()
            
            elif token_type == "IDENTIFIER":
                select_list.append(token_value)
                logger.debug(f"Added '{token_value}' to SELECT list")
                self.advance()
            
            elif token_type == "COMMA":
                logger.debug("Found comma in SELECT list, expecting more columns")
                self.advance()  # Move past the comma
                continue
            else:
                break
        
        if not select_list:
            logger.error("No columns found in SELECT list")
            raise SyntaxError("No columns found in SELECT list")
        
        logger.info(f"Finished parsing SELECT list: {select_list}")
        return select_list
    
    def parse_where_clause(self):
        column_token = self.current_token()
        
        if not column_token or column_token[0] != "IDENTIFIER":
            raise SyntaxError("Expected column name in WHERE clause")
        column_token = column_token[1]
        self.advance()
        
        operator_token = self.current_token()
        if not operator_token or operator_token[0] != "OPERATOR":
            raise SyntaxError("Expected operator in WHERE clause")
        operator = operator_token[1]
        self.advance()
        
        value_token = self.current_token()
        if not value_token or value_token[0] not in ("STRING", "NUMBER"):
            raise SyntaxError("Expected STRING or NUMBER in WHERE clause")
        value = value_token[1]
        self.advance()
        
        return {
            "column": column_token,
            "operator": operator,
            "value": value
        }
