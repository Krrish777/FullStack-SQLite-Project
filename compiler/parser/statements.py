from utils.logger import get_logger

logger = get_logger(__name__)

def parse_statement(parser):
    """
    Dispatches to the appropriate parser function based on the first keyword
    of the SQL input. Supports SELECT, INSERT, DELETE, CREATE, and UPDATE statements.

    Args:
        parser: The parser object responsible for managing tokens.

    Returns:
        A dictionary representing the parsed SQL statement.

    Raises:
        SyntaxError: If the input is empty or the keyword is unknown.
    """
    tok = parser.current_token()
    if not tok:
        raise SyntaxError("Empty input")
    _, kw = tok
    logger.info(f"Dispatching {kw}")
    if kw == "SELECT":
        return parse_select_statement(parser)
    if kw == "INSERT":
        return parse_insert_statement(parser)
    if kw == "DELETE":
        return parse_delete_statement(parser)
    if kw == "CREATE":
        return parse_create_statement(parser)
    if kw == "UPDATE":
        return parse_update_statement(parser)
    if kw == "DROP":
        return parse_drop_statement(parser)
    raise SyntaxError(f"Unknown statement: {kw}")

def parse_select_statement(parser):
    """
    Parses a SELECT statement including optional WHERE clause.

    Args:
        parser: The parser object.

    Returns:
        A dictionary containing SELECT statement structure.

    Raises:
        SyntaxError: If syntax rules are violated.
    """
    
    logger.info("Parsing SELECT statement")
    parser.expect("KEYWORD", "SELECT")
    
    cols = parser.parse_select_list()
    parser.expect("KEYWORD", "FROM")
    
    tok = parser.current_token()
    
    if not tok or tok[0] != "IDENTIFIER":
        logger.error("Expected table name after FROM")
        raise SyntaxError("Expected table name after FROM")
    
    table = tok[1]; parser.advance()
    where = None
    if parser.match("KEYWORD","WHERE"):
        where = parser.parse_where_clause()
        
    parser.expect("SEMICOLON")
    logger.info(f"Parsed SELECT on table {table} with columns {cols} and where {where}")
    return {"type":"SELECT","columns":cols,"table":table,"where":where}

def parse_insert_statement(parser):
    """
    Parses an INSERT INTO statement with optional column list.

    Args:
        parser: The parser object.

    Returns:
        A dictionary containing INSERT statement structure.

    Raises:
        SyntaxError: If syntax rules are violated.
    """
    logger.info("Parsing INSERT statement")
    parser.expect("KEYWORD","INSERT")
    parser.expect("KEYWORD","INTO")
    tok = parser.current_token()
    if tok and tok[0]=="IDENTIFIER":
        table = tok[1]; parser.advance()
    else:
        logger.error("Expected table name after INTO")
        raise SyntaxError("Expected table name after INTO")
    cols = None
    if parser.match("LPAREN"):
        cols=[]
        while True:
            tok=parser.current_token()
            if not tok or tok[0]!="IDENTIFIER":
                logger.error("Expected column name in INSERT")
                raise SyntaxError("Expected column name in INSERT")
            cols.append(tok[1]); parser.advance()
            if parser.match("COMMA"): continue
            break
        parser.expect("RPAREN")
        
    parser.expect("KEYWORD","VALUES")
    parser.expect("LPAREN")
    vals=[]
    while True:
        tok=parser.current_token()
        if not tok or tok[0] not in ("STRING","NUMBER"):
            logger.error("Expected value in INSERT")
            raise SyntaxError("Expected value in INSERT")
        vals.append(tok[1]); parser.advance()
        if parser.match("COMMA"): continue
        break
    parser.expect("RPAREN")
    parser.expect("SEMICOLON")
    logger.info(f"Parsed INSERT into {table} with columns {cols} and values {vals}")
    return {"type":"INSERT","table":table,"columns":cols,"values":vals}

def parse_delete_statement(parser):
    """
    Parses a DELETE FROM statement with optional WHERE clause.

    Args:
        parser: The parser object.

    Returns:
        A dictionary containing DELETE statement structure.

    Raises:
        SyntaxError: If syntax rules are violated.
    """
    logger.info("Parsing DELETE statement")
    parser.expect("KEYWORD","DELETE")
    parser.expect("KEYWORD","FROM")
    tok=parser.current_token()
    if not tok or tok[0]!="IDENTIFIER":
        logger.error("Expected table name in DELETE")
        raise SyntaxError("Expected table name in DELETE")
    table=tok[1]; parser.advance()
    where=None
    if parser.match("KEYWORD","WHERE"):
        where=parser.parse_where_clause()
    parser.expect("SEMICOLON")
    logger.info(f"Parsed DELETE from {table} with where {where}")
    return {"type":"DELETE","table":table,"where":where}

def parse_create_statement(parser):
    """
    Parses a CREATE TABLE statement including column definitions.

    Args:
        parser: The parser object.

    Returns:
        A dictionary containing CREATE TABLE statement structure.

    Raises:
        SyntaxError: If syntax rules are violated or type is unknown.
    """
    logger.info("Parsing CREATE statement")
    parser.expect("KEYWORD","CREATE")
    parser.expect("KEYWORD","TABLE")
    tok=parser.current_token()
    if not tok or tok[0]!="IDENTIFIER":
        logger.error("Expected table name in CREATE")
        raise SyntaxError("Expected table name in CREATE")
    table=tok[1]; parser.advance()
    parser.expect("LPAREN")
    cols=[]
    valid={"INT","VARCHAR","TEXT","DATE","FLOAT","DOUBLE"}
    while True:
        tok=parser.current_token()
        if not tok or tok[0]!="IDENTIFIER":
            break
        name=tok[1]; parser.advance()
        tok=parser.current_token()
        if not tok or tok[0]!="IDENTIFIER":
            logger.error("Expected type in CREATE")
            raise SyntaxError("Expected type in CREATE")
        typ=tok[1].upper()
        if typ not in valid:
            logger.error(f"Unknown type {typ} in CREATE")
            raise SyntaxError(f"Unknown type {typ}")
        parser.advance()
        cols.append((name,typ))
        if not parser.match("COMMA"):
            break
    parser.expect("RPAREN")
    parser.expect("SEMICOLON")
    logger.info(f"Parsed CREATE TABLE {table} with columns {cols}")
    return {"type":"CREATE","table":table,"columns":cols}

def parse_update_statement(parser):
    """
    Parses an UPDATE statement with SET clauses and optional WHERE clause.

    Args:
        parser: The parser object.

    Returns:
        A dictionary containing UPDATE statement structure.

    Raises:
        SyntaxError: If syntax rules are violated.
    """
    logger.info("Parsing UPDATE statement")
    parser.expect("KEYWORD","UPDATE")
    tok=parser.current_token()
    if not tok or tok[0]!="IDENTIFIER":
        logger.error("Expected table name in UPDATE")
        raise SyntaxError("Expected table name in UPDATE")
    table=tok[1]; parser.advance()
    parser.expect("KEYWORD","SET")
    set=[]
    while True:
        tok=parser.current_token()
        if not tok or tok[0]!="IDENTIFIER":
            break
        col=tok[1]; parser.advance()
        parser.expect("OPERATOR","=")
        tok=parser.current_token()
        if not tok or tok[0] not in ("STRING","NUMBER"):
            logger.error("Expected value in UPDATE")
            raise SyntaxError("Expected value in UPDATE")
        val=tok[1]; parser.advance()
        set.append((col,val))
        if not parser.match("COMMA"):
            break
    where=None
    if parser.match("KEYWORD","WHERE"):
        where=parser.parse_where_clause()
    parser.expect("SEMICOLON")
    logger.info(f"Parsed UPDATE {table} set {set} with where {where}")
    return {"type":"UPDATE","table":table,"set":set,"where":where}

def parse_drop_statement(parser):
    """
    Parses a DROP TABLE statement into an AST.
    Example SQL: DROP TABLE users;
    """
    logger.info("Parsing DROP TABLE statement")

    parser.expect("KEYWORD", "DROP")
    parser.expect("KEYWORD", "TABLE")
    table_name = parser.expect("IDENTIFIER")
    parser.expect("SEMICOLON")

    logger.info(f"Parsed DROP TABLE {table_name}")
    return {
        "type": "DROP",
        "table": table_name
    }