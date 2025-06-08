from core.virtual_machine import VirtualMachine
from compiler.code_generator.opcode import Opcode
import os
import shutil

# Reset the table file for a clean test run
if os.path.exists("users.tbl"):
    os.remove("users.tbl")

def has_enough_space(path, required_bytes):
    dir_path = os.path.dirname(path) or "."
    total, used, free = shutil.disk_usage(dir_path)
    return free > required_bytes

# Insert dummy rows
insert_plan = [
    (Opcode.OPEN_TABLE, "users"),
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

# Check disk space before running bulk inserts
required_bytes = 10 * 1024 * 1024  # Require at least 10MB free (adjust as needed)
if not has_enough_space("users.tbl", required_bytes):
    raise RuntimeError("Not enough disk space for database operations!")

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

# 6. Bulk insert to force B-tree splits (multi-page validation)
bulk_insert_plan = [(Opcode.OPEN_TABLE, "users")]
for i in range(1, 50):  # Insert 49 rows (adjust as needed for your page size)
    bulk_insert_plan.extend([
        (Opcode.LOAD_CONST, f"User{i}"),
        (Opcode.LOAD_CONST, 20 + (i % 30)),
        (Opcode.INSERT_ROW, "users"),
    ])
vm_bulk = VirtualMachine(bulk_insert_plan)
vm_bulk.run()

# 6b. Insert even more rows to force more splits
bulk_insert_plan2 = [(Opcode.OPEN_TABLE, "users")]
for i in range(1, 201):  # Insert 200 rows
    bulk_insert_plan2.extend([
        (Opcode.LOAD_CONST, f"User{i}"),
        (Opcode.LOAD_CONST, 20 + (i % 30)),
        (Opcode.INSERT_ROW, "users"),
    ])
vm_bulk2 = VirtualMachine(bulk_insert_plan2)
vm_bulk2.run()

# Log file size and disk usage
size = os.path.getsize("users.tbl")
dir_path = os.path.dirname("users.tbl") or "."
total, used, free = shutil.disk_usage(dir_path)
print(f"\nusers.tbl size after 200-row bulk insert: {size} bytes")
print(f"Disk free: {free // (1024*1024)} MB, used: {used // (1024*1024)} MB, total: {total // (1024*1024)} MB")

# 7. Check .tbl file size
tbl_size = os.path.getsize("users.tbl")
print(f"\nusers.tbl size after bulk insert: {tbl_size} bytes")

# 7b. SELECT WHERE rowid=150
plan_select_150 = [
    (Opcode.OPEN_TABLE, "users"),
    (Opcode.SCAN_START,),
    (Opcode.LABEL, "loop"),
    (Opcode.SCAN_NEXT,),
    (Opcode.JUMP_IF_FALSE, "end"),
    (Opcode.LOAD_COLUMN, "rowid"),
    (Opcode.LOAD_CONST, 150),
    (Opcode.COMPARE_EQ,),
    (Opcode.JUMP_IF_FALSE, "loop"),
    (Opcode.EMIT_ROW, ["rowid", "name", "age"]),
    (Opcode.JUMP, "end"),
    (Opcode.LABEL, "end"),
    (Opcode.SCAN_END,),
]
vm = VirtualMachine(plan_select_150)
vm.run()
print("\nSELECT WHERE rowid=150:")
for row in vm.output:
    print(row)


# 8. Scan all rows and check order
print("\nAll rows after bulk insert:")
vm = VirtualMachine(plan_select_all)
vm.run()
for row in vm.output:
    print(row)
    
# 9. Persistence test: comment out inserts, rerun scan after restart
print("\nAll rows after restart (persistence test):")
vm = VirtualMachine(plan_select_all)
vm.run()
for row in vm.output:
    print(row)

rowids = [row["rowid"] for row in vm.output]
assert rowids == sorted(rowids), "Rowids are not in order!"
assert len(rowids) >= 49, "Not all rows are present after bulk insert!"