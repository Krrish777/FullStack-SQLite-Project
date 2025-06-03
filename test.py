from compiler.code_generator import generate
from utils.pretty_printer import pretty_print_plan

ast = {
    "type": "DROP",
    "table": "users"
}

plan = generate(ast)
pretty_print_plan(plan)

