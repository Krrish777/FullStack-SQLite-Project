import sys
import typer
import importlib
import os
import shutil

from compiler.tokenizer import Tokenizer
from compiler.parser.statements import parse_statement
from compiler.parser import Parser
from compiler.code_generator import generate
from core.virtual_machine import VirtualMachine

from utils.errors import TokenizationError
from utils.logger import get_logger

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"

# Try to import rich and pyfiglet for enhanced output
try:
    from rich.console import Console
    from rich.prompt import Prompt
    from rich.text import Text
    console = Console()
    use_rich = True
except ImportError:
    use_rich = False
    console = None

try:
    import pyfiglet
    use_figlet = True
except ImportError:
    use_figlet = False

DATABASES_ROOT = os.path.join(os.path.dirname(__file__), "database")
current_db = None  # Global variable to track selected DB
app = typer.Typer(add_completion=False)

def print_colored(text: str, color=RESET, bold=False):
    if use_rich:
        style = "bold " if bold else ""
        if color == RED:
            style += "red"
        elif color == GREEN:
            style += "green"
        elif color == YELLOW:
            style += "yellow"
        elif color == CYAN:
            style += "cyan"
        elif color == MAGENTA:
            style += "magenta"
        else:
            style += "white"
        console.print(text, style=style)
    else:
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

def splash_screen():
    logo = "SQLite Clone"
    if use_figlet:
        logo = pyfiglet.figlet_format("SQLite Clone",)
    if use_rich:
        console.print(f"[bold magenta]{logo}[/bold magenta]")
        console.print("Author: Krish Sharma | Version: 0.1.0", style="bold cyan")
        console.print("Tip: Type .exit or .quit to quit", style="yellow")
    else:
        print_colored(logo, color=MAGENTA, bold=True)
        print_colored("Author: Krish Sharma | Version: 0.1.0", color=CYAN, bold=True)
        print_colored("Tip: Type .exit or .quit to quit", color=YELLOW)

def get_db_path(db_name):
    return os.path.join(DATABASES_ROOT, db_name)

def get_active_db_path():
    global current_db
    if not current_db:
        return None
    return get_db_path(current_db)

def ensure_databases_root():
    os.makedirs(DATABASES_ROOT, exist_ok=True)

# --- Internal Database Management Functions ---
def create_database(name: str):
    ensure_databases_root()
    db_path = get_db_path(name)
    if os.path.exists(db_path):
        print_colored(f"Database '{name}' already exists.", color=YELLOW, bold=True)
        raise typer.Exit(1)
    os.makedirs(db_path)
    open(os.path.join(db_path, "__catalog.tbl"), "wb").close()
    print_colored(f"Database '{name}' created.", color=GREEN, bold=True)

def delete_database(name: str):
    db_path = get_db_path(name)
    if not os.path.exists(db_path):
        print_colored(f"Database '{name}' does not exist.", color=RED, bold=True)
        raise typer.Exit(1)
    shutil.rmtree(db_path)
    global current_db
    if current_db == name:
        current_db = None
    print_colored(f"Database '{name}' deleted.", color=GREEN, bold=True)

def list_databases():
    ensure_databases_root()
    dbs = [d for d in os.listdir(DATABASES_ROOT) if os.path.isdir(get_db_path(d))]
    print_colored("\nDatabases:", color=YELLOW, bold=True)
    for db in dbs:
        print_colored(db, color=CYAN)

def use_database(name: str):
    db_path = get_db_path(name)
    if not os.path.exists(db_path):
        print_colored(f"Database '{name}' does not exist.", color=RED, bold=True)
        raise typer.Exit(1)
    global current_db
    current_db = name
    print_colored(f"Now using database '{name}'.", color=GREEN, bold=True)

def show_all_tables():
    db_path = get_active_db_path()
    if not db_path:
        print_colored("No active database selected. Use 'use-db <name>' to continue.", color=RED, bold=True)
        raise typer.Exit(1)
    tbls = [f for f in os.listdir(db_path) if f.endswith('.tbl') and f != "__catalog.tbl"]
    print_colored("\nTables:", color=YELLOW, bold=True)
    for t in tbls:
        print_colored(t[:-4], color=CYAN)

# --- Database Management Commands ---
@app.command()
def create_db(name: str):
    """Create a new database."""
    create_database(name)

@app.command()
def delete_db(name: str):
    """Delete a database and all its tables."""
    delete_database(name)

@app.command()
def list_dbs():
    """List all databases."""
    list_databases()

@app.command()
def use_db(name: str):
    """Select a database for this session."""
    use_database(name)

@app.command()
def show_tables():
    """List all tables in the current database."""
    show_all_tables()

def get_prompt():
    global current_db
    if current_db:
        return f"{current_db}>"
    else:
        return ">"

def process_sql(sql, tokenizer, logger):
    db_path = get_active_db_path()
    if not db_path:
        print_colored("No active database selected. Use 'use-db <name>' to continue.", color=RED, bold=True)
        return
    try:
        tokens = tokenizer.tokenize(sql)
        print_colored("\nTokens:", color=YELLOW, bold=True)
        for token_type, token_value in tokens:
            print(f" {BOLD}{token_type:<12}{RESET}: {token_value}")
        print_colored("\nTokenization successful!", color=GREEN, bold=True)

        parser = Parser(tokens)
        parse_tree = parse_statement(parser)

        print_colored("\nParse Tree:", color=CYAN, bold=True)
        print_tree(parse_tree)

        codegen = generate(parse_tree)
        print_colored("\nGenerated Code:", color=MAGENTA, bold=True)
        for opcode, *args in codegen:
            args_str = ", ".join(map(str, args))
            print(f"{opcode.name}({args_str})")

        # Pass db_path to VirtualMachine
        vm = VirtualMachine(codegen, db_path=db_path)
        vm.run()
        if vm.output:
            print_colored("\nVM Output:", color=GREEN, bold=True)
            # Try to display as Rich Table if possible
            if use_rich and isinstance(vm.output, list) and vm.output:
                from rich.table import Table
                # If output is list of dicts
                if isinstance(vm.output[0], dict):
                    columns = list(vm.output[0].keys())
                    table = Table(show_header=True, header_style="bold magenta")
                    for col in columns:
                        table.add_column(str(col), style="cyan")
                    for row in vm.output:
                        table.add_row(*(str(row.get(col, "")) for col in columns))
                    console.print(table)
                # If output is list of lists/tuples
                elif isinstance(vm.output[0], (list, tuple)):
                    table = Table(show_header=False)
                    for _ in range(len(vm.output[0])):
                        table.add_column()
                    for row in vm.output:
                        table.add_row(*(str(cell) for cell in row))
                    console.print(table)
                else:
                    for output in vm.output:
                        print(output)
            else:
                for output in vm.output:
                    print(output)
        elif parse_tree.get("type") == "INSERT":
            print_colored("\nInsert operation completed successfully.", color=GREEN, bold=True)
        elif parse_tree.get("type") == "CREATE":
            print_colored("\nTable created successfully.", color=GREEN, bold=True)
        elif parse_tree.get("type") == "DROP":
            print_colored("\nTable dropped successfully.", color=GREEN, bold=True)
    except TokenizationError as e:
        logger.error(f"Tokenization error: {e}")
        print_colored(f"Tokenization error: {e}", color=RED, bold=True)
    except SyntaxError as e:
        logger.error(f"Syntax error: {e}")
        print_colored(f"Syntax error: {e}", color=RED, bold=True)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print_colored(f"Unexpected error: {e}", color=RED, bold=True)

def show_commands():
    commands = [
        ".exit   - Exit the shell",
        ".quit   - Exit the shell",
        ".help   - Show this help message",
        ".commands - Show supported SQL commands",
    ]
    print_colored("\nSupported shell commands:", color=YELLOW, bold=True)
    for cmd in commands:
        print_colored(cmd, color=CYAN)

def show_sql_help():
    sql_statements = [
        "CREATE TABLE ...",
        "DROP TABLE ...",
        "INSERT INTO ...",
        "SELECT ...",
        "UPDATE ...",
        "DELETE FROM ...",
        # Add more supported SQL statements as you implement them
    ]
    print_colored("\nSupported SQL statements:", color=YELLOW, bold=True)
    for stmt in sql_statements:
        print_colored(stmt, color=CYAN)

def handle_meta_command(cmd: str):
    import shlex
    tokens = shlex.split(cmd)
    if not tokens:
        return
    command = tokens[0].lower()
    args = tokens[1:]
    try:
        if command in {'.create-db', '.createdb'}:
            if len(args) != 1:
                print_colored("Usage: .create-db <name>", color=YELLOW, bold=True)
            else:
                create_database(args[0])
        elif command in {'.delete-db', '.deletedb'}:
            if len(args) != 1:
                print_colored("Usage: .delete-db <name>", color=YELLOW, bold=True)
            else:
                delete_database(args[0])
        elif command in {'.list-dbs', '.listdbs'}:
            if args:
                print_colored("Usage: .list-dbs", color=YELLOW, bold=True)
            else:
                list_databases()
        elif command in {'.use-db', '.usedb'}:
            if len(args) != 1:
                print_colored("Usage: .use-db <name>", color=YELLOW, bold=True)
            else:
                use_database(args[0])
        elif command in {'.show-tables', '.showtables'}:
            if args:
                print_colored("Usage: .show-tables", color=YELLOW, bold=True)
            else:
                show_all_tables()
        elif command in {'.help', '.commands'}:
            show_meta_commands()
        else:
            print_colored(f"Unknown meta-command: {cmd}", color=RED, bold=True)
    except typer.Exit:
        pass
    except Exception as e:
        print_colored(f"Error: {e}", color=RED, bold=True)

def show_meta_commands():
    meta_cmds = [
        ".create-db <name>   - Create a new database",
        ".delete-db <name>   - Delete a database",
        ".list-dbs           - List all databases",
        ".use-db <name>      - Select a database for this session",
        ".show-tables        - List all tables in the current database",
        ".help               - Show this help message",
        ".commands           - Show this help message",
        ".exit, .quit        - Exit the shell",
    ]
    print_colored("\nMeta-commands:", color=YELLOW, bold=True)
    for cmd in meta_cmds:
        print_colored(cmd, color=CYAN)

@app.command()
def main(commands: bool = typer.Option(False, "--commands", help="Show supported shell commands and exit.")):
    """Start the interactive SQL shell or show supported commands."""
    if commands:
        show_commands()
        raise typer.Exit()
    logger = get_logger(__name__)
    tokenizer = Tokenizer()
    splash_screen()
    show_meta_commands()
    ensure_databases_root()
    while True:
        try:
            if use_rich:
                sql = Prompt.ask(f"[bold green]{get_prompt()}[/bold green]")
            else:
                sql = input(f"{GREEN}{get_prompt()}{RESET} ")
            sql = sql.strip()
            if sql.lower() in {".exit", ".quit"}:
                print_colored("Goodbye!", color=CYAN, bold=True)
                break
            if sql.lower() == ".help":
                show_meta_commands()
                continue
            if sql.lower() == ".commands":
                show_meta_commands()
                continue
            if sql.startswith(".") and sql.lower() not in {".exit", ".quit", ".help", ".commands"}:
                handle_meta_command(sql)
                continue
            if not sql:
                continue
            process_sql(sql, tokenizer, logger)
        except (KeyboardInterrupt, EOFError):
            print()
            print_colored("Goodbye!", color=CYAN, bold=True)
            break

def interactive_shell():
    logger = get_logger(__name__)
    tokenizer = Tokenizer()
    splash_screen()
    show_meta_commands()
    ensure_databases_root()
    while True:
        try:
            if use_rich:
                sql = Prompt.ask(f"[bold green]{get_prompt()}[/bold green]")
            else:
                sql = input(f"{GREEN}{get_prompt()}{RESET} ")
            sql = sql.strip()
            if sql.lower() in {".exit", ".quit"}:
                print_colored("Goodbye!", color=CYAN, bold=True)
                break
            if sql.lower() == ".help":
                show_meta_commands()
                continue
            if sql.lower() == ".commands":
                show_meta_commands()
                continue
            if sql.startswith(".") and sql.lower() not in {".exit", ".quit", ".help", ".commands"}:
                handle_meta_command(sql)
                continue
            if not sql:
                continue
            process_sql(sql, tokenizer, logger)
        except (KeyboardInterrupt, EOFError):
            print()
            print_colored("Goodbye!", color=CYAN, bold=True)
            break

@app.callback(invoke_without_command=True)
def default_callback(ctx: typer.Context):
    """Launch interactive shell if no subcommand is provided."""
    if ctx.invoked_subcommand is None:
        interactive_shell()

def install_message():
    print("\n[!] For best experience, install dependencies: 'pip install typer rich pyfiglet'\n")

if __name__ == "__main__":
    if not use_rich or not use_figlet:
        install_message()
    app()  # Use Typer app entry point