def parse_statement(parser):
    token = parser.current_token()
    if token is None:
        raise SyntaxError("Unexpected end of input")
    token_type, token_value = token
    
    if token_type == "KEYWORD" and token_value == "SELECT":
        return parse_select_statement(parser)
    elif token_type == "KEYWORD" and token_value == "INSERT":
        return parse_insert_statement(parser)
    elif token_type == "KEYWORD" and token_value == "CREATE":
        return parse_create_statement(parser)
    elif token_type == "KEYWORD" and token_value == "DELETE":
        return parse_delete_statement(parser)
    elif token_type == "KEYWORD" and token_value == "UPDATE":
        return parse_update_statement(parser)
    
    else:
        raise SyntaxError(f"Unexpected token: {token_value} at position {parser.pos}")
    
def parse_select_statement(parser):
    parser.expect("KEYWORD", "SELECT")
    select_list = parser.parse_select_list()
    parser.expect("KEYWORD", "FROM")
    
    table_name = parser.current_token()
    if table_name and table_name[0] == "IDENTIFIER":
        table_name = table_name[1]
        parser.advance()
    else:
        raise SyntaxError("Expected table name after FROM")
    return {
        "type": "SELECT",
        "columns": select_list,
        "table": table_name
    }

def parse_insert_statement(parser):
    pass

def parse_create_statement(parser):
    pass

def parse_delete_statement(parser):
    pass

def parse_update_statement(parser):
    pass