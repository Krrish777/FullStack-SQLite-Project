import sys
import argparse
import json

from compiler.tokenizer import Tokenizer
from compiler.parser.statements import parse_statement
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

def print_colored(text:str, color=RESET, bold=False):
    """
    Prints the given text in color and optionally bold in the terminal.
    """
    if bold:
        print(f"{color}{BOLD}{text}{RESET}")
    else:
        print(f"{color}{text}{RESET}")

def print_tree(parse_tree, indent=0, is_last=True):
    space = "    " * indent
    branch_symbol = "`-- " if is_last else "|-- "
    
    if isinstance(parse_tree, dict):
        for i, (key, value) in enumerate(parse_tree.items()):
            is_last_item = i == len(parse_tree) - 1
            print(f"{space}{branch_symbol}{key}:")
            print_tree(value, indent + 1, is_last_item)
    elif isinstance(parse_tree, list):
        for i, item in enumerate(parse_tree):
            is_last_item = i == len(parse_tree) - 1
            print_tree(item, indent, is_last_item)
    else:
        print(f"{space}{branch_symbol}{parse_tree}")


def format_tree(parse_tree, indent=""):
    """Recursively formats a parse tree into a string representation."""
    if isinstance(parse_tree, dict):
        result = []
        for key, value in parse_tree.items():
            result.append(f"{indent}{key}:")
            if isinstance(value, dict):
                result.append(format_tree(value, indent + "  "))
            elif isinstance(value, list):
                for item in value:
                    result.append(format_tree(item, indent + "  "))
            else:
                result.append(f"{indent}  {value}")
        return "\n".join(result)
    else:
        return f"{indent}{parse_tree}"

logger = get_logger(__name__)

if __name__ == "__main__":
    tokenizer = Tokenizer()

    parser = argparse.ArgumentParser(description="SQL Tokenizer CLI and Parser")
    parser.add_argument("sql", type=str, help="SQL query to tokenize and parse")
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
        print_tree(parse_tree)  # Print the formatted tree structure with branch symbols

    except TokenizationError as e:
        logger.error(f"Tokenization error: {e}")
        print_colored(f"Tokenization error: {e}", color=RED, bold=True)

    except SyntaxError as e:
        logger.error(f"Syntax error: {e}")
        print_colored(f"Syntax error: {e}", color=RED, bold=True)