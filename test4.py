from core.virtual_machine import VirtualMachine
from compiler.code_generator.opcode import Opcode

# 1. Create a table using op_create_table
create_table_plan = [
    (Opcode.CREATE_TABLE, "users", [("name", "TEXT"), ("age", "INT")]),
]
vm = VirtualMachine(create_table_plan)
vm.run()

# 2. Insert some rows
insert_plan = [
    (Opcode.LOAD_CONST, "Alice"),
    (Opcode.LOAD_CONST, 35),
    (Opcode.INSERT_ROW, "users"),
    (Opcode.LOAD_CONST, "Bob"),
    (Opcode.LOAD_CONST, 25),
    (Opcode.INSERT_ROW, "users"),
]
vm = VirtualMachine(insert_plan)
vm.run()

# 3. Select all rows
select_plan = [
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
vm = VirtualMachine(select_plan)
vm.run()
print("All rows after create/insert:")
for row in vm.output:
    print(row)

# 4. Simulate restart and select again (persistence test)
vm = VirtualMachine(select_plan)
vm.run()
print("All rows after restart:")
for row in vm.output:
    print(row)
