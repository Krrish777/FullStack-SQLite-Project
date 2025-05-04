from utils.logger import get_logger
logger = get_logger(__name__)


def parse_statement(parser):
    logger.info("Starting parsing statement")
    token = parser.current_token()
    if token is None:
        logger.error("Unexpected end of input")
        raise SyntaxError("Unexpected end of input")
    
    token_type, token_value = token
    logger.debug(f"Current token: {token}, value: {token_value}")
    
    if token_type == "KEYWORD" and token_value == "SELECT":
        logger.debug("Parsing SELECT statement")
        return parse_select_statement(parser)
    
    elif token_type == "KEYWORD" and token_value == "INSERT":
        logger.debug("Parsing INSERT statement")
        return parse_insert_statement(parser)
    
    elif token_type == "KEYWORD" and token_value == "CREATE":
        logger.debug("Parsing CREATE statement")
        return parse_create_statement(parser)
    
    elif token_type == "KEYWORD" and token_value == "DELETE":
        logger.debug("Parsing DELETE statement")
        return parse_delete_statement(parser)
    
    elif token_type == "KEYWORD" and token_value == "UPDATE":
        logger.debug("Parsing UPDATE statement")
        return parse_update_statement(parser)
    
    else:
        logger.error(f"Unexpected token: {token_value} at position {parser.pos}")
        raise SyntaxError(f"Unexpected token: {token_value} at position {parser.pos}")
    
def parse_select_statement(parser):
    logger.debug("Parsing SELECT statement")
    parser.expect("KEYWORD", "SELECT")
    select_list = parser.parse_select_list()
    parser.expect("KEYWORD", "FROM")
    
    table_name = parser.current_token()
    if table_name and table_name[0] == "IDENTIFIER":
        table_name = table_name[1]
        parser.advance()
    else:
        logger.error("Expected table name after FROM")
        raise SyntaxError("Expected table name after FROM")
    
    where_clause = None
    if parser.match("KEYWORD", "WHERE"):
        where_clause = parser.parse_where_clause()
    
    parser.expect("SEMICOLON")
    logger.debug(f"Parsed SELECT statement: {select_list}, table: {table_name}, where: {where_clause}")
    return {
        "type": "SELECT",
        "columns": select_list,
        "table": table_name,
        "where": where_clause
    }

def parse_insert_statement(parser):
    logger.debug("Parsing INSERT statement")
    parser.expect("KEYWORD", "INSERT")
    parser.expect("KEYWORD", "INTO")
    
    table_name = parser.current_token()
    if table_name and table_name[0] == "IDENTIFIER":
        table_name = table_name[1]
        parser.advance()
    else:
        logger.error("Expected table name after INTO")
        raise SyntaxError("Expected table name after INTO")
    
    parser.expect("KEYWORD", "VALUES")
    parser.expect("LPAREN")
    
    values = []
    while True:
        token = parser.current_token()
        if token is None :
            logger.error("Unexpected end of input while parsing INSERT statement")
            raise SyntaxError("Unexpected end of input")
        
        token_type, token_value = token
        
        if token_type in ("STRING", "NUMBER"):
            values.append(token_value)
            parser.advance()
        else:
            logger.error(f"Expected STRING or NUMBER but got {token_type} at position {parser.pos}")
            raise SyntaxError(f"Expected STRING or NUMBER but got {token_type} at position {parser.pos}")
        
        if parser.match("COMMA"):
            continue
        else:
            break
    parser.expect("RPAREN")
    parser.expect("SEMICOLON")
    logger.debug(f"Parsed INSERT statement: table: {table_name}, values: {values}")
    return {
        "type": "INSERT",
        "table": table_name,
        "values": values
    }

def parse_delete_statement(parser):
    logger.debug("Parsing DELETE statement")
    parser.expect("KEYWORD", "DELETE")
    parser.expect("KEYWORD", "FROM")
    
    table_name = parser.current_token()
    if table_name and table_name[0] == "IDENTIFIER":
        table_name = table_name[1]
        parser.advance()
    else:
        logger.error("Expected table name after FROM")
        raise SyntaxError("Expected table name after FROM")
    
    where_clause = None
    if parser.match("KEYWORD", "WHERE"):
        where_clause = parser.parse_where_clause()
        
    parser.expect("SEMICOLON")
    logger.debug(f"Parsed DELETE statement: table: {table_name}, where: {where_clause}")    
    return {
        "type": "DELETE",
        "table": table_name,
        "where": where_clause
    }

def parse_create_statement(parser):
    logger.debug("Parsing CREATE statement")
    parser.expect("KEYWORD", "CREATE")
    parser.expect("KEYWORD", "TABLE")
    
    table_name_token = parser.current_token()
    if table_name_token and table_name_token[0] == "IDENTIFIER":
        table_name = table_name_token[1]
        parser.advance()
    else:
        logger.error("Expected table name after CREATE TABLE")
        raise SyntaxError("Expected table name after CREATE TABLE")
        
    columns = []
    parser.expect("LPAREN")
    
    valid_types = {"INT", "VARCHAR", "TEXT", "DATE", "FLOAT", "DOUBLE"}
    
    while True:
        token = parser.current_token()
        if token is None:
            logger.error("Unexpected end of input while parsing CREATE statement")
            raise SyntaxError("Unexpected end of input")
        
        token_type, token_value = token
        
        if token_type == "IDENTIFIER":
            column_name = token_value
            parser.advance()
        else:
            logger.error(f"Expected column name but got {token_type} at position {parser.pos}")
            raise SyntaxError(f"Expected column name but got {token_type} at position {parser.pos}")
        
        token = parser.current_token()
        if token and token[0] == "IDENTIFIER":
            column_type = token[1].upper()
        else:
            logger.error(f"Expected column type after column name but got {token_type} at position {parser.pos}")
            raise SyntaxError(f"Expected column type after column name but got {token_type} at position {parser.pos}")

        if column_type not in valid_types:
            logger.error(f"Invalid column type: {column_type} at position {parser.pos}")
            raise SyntaxError(f"Invalid column type: {column_type} at position {parser.pos}")
        
        parser.advance()  # only one advance is needed
        
        columns.append((column_name, column_type))
        
        if parser.match("COMMA"):
            continue
        else:
            break
        logger.debug(f"Added column: {column_name} of type: {column_type}")
        
    parser.expect("RPAREN")
    parser.expect("SEMICOLON")
    
    return {
        "type": "CREATE",
        "table": table_name,
        "columns": columns
    }