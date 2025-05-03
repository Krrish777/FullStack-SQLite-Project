import sys
import argparse

from compiler.tokenizer import Tokenizer
from compiler.statements import parse_statement
from compiler.parser import Parser

from utils.errors import TokenizationError
from utils.logger import get_logger

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"

def print_colored(text, color=RESET, bold=False):
    if bold:
        print(f"{color}{BOLD}{text}{RESET}")
    else:
        print(f"{color}{text}{RESET}")
        

logger = get_logger(__name__)

if __name__ == "__main__":
    tokenizer = Tokenizer()
    
    parser = argparse.ArgumentParser(description="SQL Tokenizer CLI and Parser")
    parser.add_argument("sql", type=str, help="SQL query to tokenize")
    args = parser.parse_args()
    
    sql = args.sql
    
    try:
        tokens = tokenizer.tokenize(sql)
        print_colored("\nTokens:", color=YELLOW, bold=True)
        for token_type, token_value in tokens:
            print(f" {BOLD}{token_type:<12}{RESET}: {token_value}")
        print_colored("\nTokenization successful!", color=GREEN, bold=True)
        
        parser = Parser(tokens)
        parse_tree = parse_statement(parser)
        
        print_colored("\nParse Tree:", color=CYAN, bold=True)
        print(parse_tree)
            
    except TokenizationError as e:
        logger.error(f"Tokenization error: {e}")
        print_colored(f"Tokenization error: {e}", color=RED, bold=True)
        
    except SyntaxError as e:
        logger.error(f"Syntax error: {e}")
        print_colored(f"Syntax error: {e}", color=RED, bold=True)
