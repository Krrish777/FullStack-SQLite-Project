from core.virtual_machine import VirtualMachine
from compiler.code_generator.opcode import Opcode
import os

# Reset the table file for a clean test run
if os.path.exists("users.tbl"):
    os.remove("users.tbl")

# Insert dummy rows
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

# 1. Show all rows
print("All rows after insert:")
plan_select_all = [
    (Opcode.OPEN_TABLE, "users"),
    (Opcode.SCAN_START,),
    (Opcode.LABEL, "loop"),
    (Opcode.SCAN_NEXT,),
    (Opcode.JUMP_IF_FALSE, "end"),
    (Opcode.EMIT_ROW, ["rowid", "name", "age"]),
    (Opcode.JUMP, "loop"),
    (Opcode.LABEL, "end"),
    (Opcode.SCAN_END,),
]
vm = VirtualMachine(plan_select_all)
vm.run()
for row in vm.output:
    print(row)

# 2. Update Alice's age from 35 to 99
plan_update = [
    (Opcode.OPEN_TABLE, "users"),
    (Opcode.SCAN_START,),
    (Opcode.LABEL, "loop"),
    (Opcode.SCAN_NEXT,),
    (Opcode.JUMP_IF_FALSE, "end"),
    (Opcode.LOAD_COLUMN, "name"),
    (Opcode.LOAD_CONST, "Alice"),
    (Opcode.COMPARE_EQ,),
    (Opcode.LOAD_COLUMN, "age"),
    (Opcode.LOAD_CONST, 35),
    (Opcode.COMPARE_EQ,),
    (Opcode.LOGICAL_AND,),
    (Opcode.JUMP_IF_FALSE, "loop"),
    (Opcode.LOAD_CONST, 99),  # new age
    (Opcode.UPDATE_COLUMN, "age"),
    (Opcode.UPDATE_ROW,),
    (Opcode.JUMP, "loop"),
    (Opcode.LABEL, "end"),
    (Opcode.SCAN_END,),
]
vm = VirtualMachine(plan_update)
vm.run()

# 3. Show all rows after update
print("\nAll rows after update (Alice age 35 -> 99):")
vm = VirtualMachine(plan_select_all)
vm.run()
for row in vm.output:
    print(row)

# 4. Delete Bob
plan_delete = [
    (Opcode.OPEN_TABLE, "users"),
    (Opcode.SCAN_START,),
    (Opcode.LABEL, "loop"),
    (Opcode.SCAN_NEXT,),
    (Opcode.JUMP_IF_FALSE, "end"),
    (Opcode.LOAD_COLUMN, "name"),
    (Opcode.LOAD_CONST, "Bob"),
    (Opcode.COMPARE_EQ,),
    (Opcode.JUMP_IF_FALSE, "loop"),
    (Opcode.DELETE_ROW,),
    (Opcode.JUMP, "loop"),
    (Opcode.LABEL, "end"),
    (Opcode.SCAN_END,),
]
vm = VirtualMachine(plan_delete)
vm.run()

# 5. Show all rows after delete
print("\nAll rows after deleting Bob:")
vm = VirtualMachine(plan_select_all)
vm.run()
for row in vm.output:
    print(row)