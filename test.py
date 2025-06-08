from core.virtual_machine import VirtualMachine
from compiler.code_generator.opcode import Opcode
import os

# Optional: Reset the table file for a clean test run
if os.path.exists("users.tbl"):
    os.remove("users.tbl")

# Insert multiple dummy rows
insert_plan = [
    (Opcode.LOAD_CONST, "Alice"),
    (Opcode.LOAD_CONST, 35),
    (Opcode.INSERT_ROW, "users"),
    (Opcode.LOAD_CONST, "Bob"),
    (Opcode.LOAD_CONST, 25),
    (Opcode.INSERT_ROW, "users"),
    (Opcode.LOAD_CONST, "Alice"),
    (Opcode.LOAD_CONST, 20),
    (Opcode.INSERT_ROW, "users"),
    (Opcode.LOAD_CONST, "Charlie"),
    (Opcode.LOAD_CONST, 40),
    (Opcode.INSERT_ROW, "users"),
]
vm_insert = VirtualMachine(insert_plan)
vm_insert.run()

# Query: WHERE age > 30 AND name == "Alice"
plan = [
    (Opcode.OPEN_TABLE, "users"),
    (Opcode.SCAN_START,),
    (Opcode.LABEL, "loop"),
    (Opcode.SCAN_NEXT,),
    (Opcode.JUMP_IF_FALSE, "end"),

    (Opcode.LOAD_COLUMN, "age"),
    (Opcode.LOAD_CONST, 30),
    (Opcode.COMPARE_GT,),

    (Opcode.LOAD_COLUMN, "name"),
    (Opcode.LOAD_CONST, "Alice"),
    (Opcode.COMPARE_EQ,),

    (Opcode.LOGICAL_AND,),

    (Opcode.JUMP_IF_FALSE, "loop"),

    (Opcode.EMIT_ROW, ["rowid", "name", "age"]),
    (Opcode.JUMP, "loop"),

    (Opcode.LABEL, "end"),
    (Opcode.SCAN_END,)
]

vm = VirtualMachine(plan)
vm.run()

print("Query Result:")
for row in vm.output:
    print(row)