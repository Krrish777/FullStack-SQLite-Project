from compiler.code_generator import generate
from utils.pretty_printer import pretty_print_plan

ast = {
    "type": "SELECT",
    "table_name": "users",
    "columns": ["id", "name"],
    "where": {
        "column": "id",
        "operator": "=",
        "value": 1
    }
}

plan = generate(ast)
pretty_print_plan(plan)
