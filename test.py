from core.virtual_machine import VirtualMachine
from compiler.code_generator.opcode import Opcode

plan = [
    (Opcode.OPEN_TABLE, "users"),
    (Opcode.SCAN_START,),
    (Opcode.LABEL, "loop"),
    (Opcode.SCAN_NEXT,),
    (Opcode.JUMP_IF_FALSE, "done"),

    (Opcode.LOAD_COLUMN, "age"),   # LHS
    (Opcode.LOAD_CONST, 25),       # RHS
    (Opcode.COMPARE_EQ,),
    (Opcode.JUMP_IF_FALSE, "loop"),

    (Opcode.EMIT_ROW, ["name", "age"]),
    (Opcode.JUMP, "loop"),
    (Opcode.LABEL, "done"),
    (Opcode.SCAN_END,)
]







vm = VirtualMachine(plan)
vm.run()
print("Query Result:")
for row in vm.output:
    print(row)

