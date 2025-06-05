from compiler.code_generator import generate
from core.virtual_machine import VirtualMachine
from utils.pretty_printer import pretty_print_plan
from utils.logger import get_logger

logger = get_logger(__name__)

def run_sql_ast(ast):
    print("\n🧠 AST:")
    print(ast)

    print("\n🛠️  Code Generation:")
    plan = generate(ast)
    pretty_print_plan(plan)

    print("\n⚙️  Virtual Machine Execution:")
    vm = VirtualMachine(plan)
    vm.run()

    if vm.output:
        print("\n📤 Output Rows:")
        for row in vm.output:
            print(row)
    else:
        print("\n📦 Final Table State:")
        for row in vm.rows:
            print(row)
    print("✅ Done\n" + "-" * 40)


if __name__ == "__main__":
    # Test case 1: SELECT
    run_sql_ast({
        "type": "SELECT",
        "table": "users",
        "columns": ["name"],
        "where": {"column": "age", "operator": ">", "value": 30}
    })

    # Test case 2: INSERT
    run_sql_ast({
        "type": "INSERT",
        "table": "users",
        "columns": ["name", "age"],
        "values": ["Lakshay", 22]
    })

    # Test case 3: UPDATE
    run_sql_ast({
        "type": "UPDATE",
        "table": "users",
        "set": [("age", 31)],
        "where": {"column": "name", "operator": "==", "value": "Lakshay"}
    })

    # Test case 4: DELETE
    run_sql_ast({
        "type": "DELETE",
        "table": "users",
        "where": {"column": "name", "operator": "==", "value": "Bob"}
    })

    # Test case 5: CREATE TABLE
    run_sql_ast({
        "type": "CREATE",
        "table": "books",
        "columns": [("id", "INT"), ("title", "TEXT")]
    })

    # Test case 6: DROP TABLE
    run_sql_ast({
        "type": "DROP",
        "table": "books"
    })
