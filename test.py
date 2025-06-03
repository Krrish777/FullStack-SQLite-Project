from compiler.code_generator import generate
from utils.pretty_printer import pretty_print_plan

ast = {
    "type": "CREATE",
    "table_name": "users",
    "columns": [("id", "INT"), ("name", "TEXT")]
}

plan = generate(ast)
pretty_print_plan(plan)
