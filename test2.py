import os
import pytest
from core.virtual_machine import VirtualMachine
from compiler.code_generator.opcode import Opcode

DB_FILE = "users.tbl"

@pytest.fixture(autouse=True)
def cleanup_db():
    # Remove the table file before and after each test for isolation
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    yield
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

def setup_vm(insert_rows=None):
    # Optionally insert initial rows
    if insert_rows:
        plan = []
        for name, age in insert_rows:
            plan.extend([
                (Opcode.LOAD_CONST, name),
                (Opcode.LOAD_CONST, age),
                (Opcode.INSERT_ROW, "users"),
            ])
        vm = VirtualMachine(plan)
        vm.run()
    return VirtualMachine([])  # Return a VM ready for further plans

def select_all():
    plan = [
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
    vm = VirtualMachine(plan)
    vm.run()
    return vm.output

def select_where_rowid(rowid):
    plan = [
        (Opcode.OPEN_TABLE, "users"),
        (Opcode.SCAN_START,),
        (Opcode.LABEL, "loop"),
        (Opcode.SCAN_NEXT,),
        (Opcode.JUMP_IF_FALSE, "end"),
        (Opcode.LOAD_COLUMN, "rowid"),
        (Opcode.LOAD_CONST, rowid),
        (Opcode.COMPARE_EQ,),
        (Opcode.JUMP_IF_FALSE, "loop"),
        (Opcode.EMIT_ROW, ["rowid", "name", "age"]),
        (Opcode.JUMP, "end"),
        (Opcode.LABEL, "end"),
        (Opcode.SCAN_END,),
    ]
    vm = VirtualMachine(plan)
    vm.run()
    return vm.output

def test_insert_and_select():
    setup_vm([("Krish", 21)])
    rows = select_all()
    print("\n[insert_and_select] rows:", rows)
    assert len(rows) == 1
    assert rows[0]["name"] == "Krish"
    assert rows[0]["age"] == 21

def test_update_persistence():
    setup_vm([("Krish", 21)])
    # Update name where rowid == 1
    plan = [
        (Opcode.OPEN_TABLE, "users"),
        (Opcode.SCAN_START,),
        (Opcode.LABEL, "loop"),
        (Opcode.SCAN_NEXT,),
        (Opcode.JUMP_IF_FALSE, "end"),
        (Opcode.LOAD_COLUMN, "rowid"),
        (Opcode.LOAD_CONST, 1),
        (Opcode.COMPARE_EQ,),
        (Opcode.JUMP_IF_FALSE, "loop"),
        (Opcode.LOAD_CONST, "Kris"),
        (Opcode.UPDATE_COLUMN, "name"),
        (Opcode.UPDATE_ROW,),
        (Opcode.JUMP, "end"),
        (Opcode.LABEL, "end"),
        (Opcode.SCAN_END,),
    ]
    vm = VirtualMachine(plan)
    vm.run()
    # Simulate restart: reload and select
    rows = select_where_rowid(1)
    print("\n[update_persistence] rows:", rows)
    assert rows[0]["name"] == "Kris"

def test_delete_persistence():
    setup_vm([("Krish", 21)])
    # Delete where rowid == 1
    plan = [
        (Opcode.OPEN_TABLE, "users"),
        (Opcode.SCAN_START,),
        (Opcode.LABEL, "loop"),
        (Opcode.SCAN_NEXT,),
        (Opcode.JUMP_IF_FALSE, "end"),
        (Opcode.LOAD_COLUMN, "rowid"),
        (Opcode.LOAD_CONST, 1),
        (Opcode.COMPARE_EQ,),
        (Opcode.JUMP_IF_FALSE, "loop"),
        (Opcode.DELETE_ROW,),
        (Opcode.JUMP, "loop"),
        (Opcode.LABEL, "end"),
        (Opcode.SCAN_END,),
    ]
    vm = VirtualMachine(plan)
    vm.run()
    # Simulate restart: reload and select
    rows = select_all()
    print("\n[delete_persistence] rows:", rows)
    assert len(rows) == 0

def test_multiple_inserts_and_select():
    setup_vm([("A", 10), ("B", 20), ("C", 30)])
    rows = select_all()
    print("\n[multiple_inserts_and_select] rows:", rows)
    assert len(rows) == 3
    names = {row["name"] for row in rows}
    assert names == {"A", "B", "C"}

def test_update_and_delete_combo():
    setup_vm([("A", 10), ("B", 20)])
    # Update B to age 99, then delete A
    plan = [
        (Opcode.OPEN_TABLE, "users"),
        (Opcode.SCAN_START,),
        (Opcode.LABEL, "loop"),
        (Opcode.SCAN_NEXT,),
        (Opcode.JUMP_IF_FALSE, "end"),
        (Opcode.LOAD_COLUMN, "name"),
        (Opcode.LOAD_CONST, "B"),
        (Opcode.COMPARE_EQ,),
        (Opcode.JUMP_IF_FALSE, "skip_update"),
        (Opcode.LOAD_CONST, 99),
        (Opcode.UPDATE_COLUMN, "age"),
        (Opcode.UPDATE_ROW,),
        (Opcode.LABEL, "skip_update"),
        (Opcode.JUMP, "loop"),
        (Opcode.LABEL, "end"),
        (Opcode.SCAN_END,),
    ]
    vm = VirtualMachine(plan)
    vm.run()
    # Delete A
    plan = [
        (Opcode.OPEN_TABLE, "users"),
        (Opcode.SCAN_START,),
        (Opcode.LABEL, "loop"),
        (Opcode.SCAN_NEXT,),
        (Opcode.JUMP_IF_FALSE, "end"),
        (Opcode.LOAD_COLUMN, "name"),
        (Opcode.LOAD_CONST, "A"),
        (Opcode.COMPARE_EQ,),
        (Opcode.JUMP_IF_FALSE, "loop"),
        (Opcode.DELETE_ROW,),
        (Opcode.JUMP, "loop"),
        (Opcode.LABEL, "end"),
        (Opcode.SCAN_END,),
    ]
    vm = VirtualMachine(plan)
    vm.run()
    # Check results
    rows = select_all()
    print("\n[update_and_delete_combo] rows:", rows)
    assert len(rows) == 1
    assert rows[0]["name"] == "B"
    assert rows[0]["age"] == 99