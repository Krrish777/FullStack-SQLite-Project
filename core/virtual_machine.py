from compiler.code_generator.opcode import Opcode
from utils.logger import get_logger

logger = get_logger(__name__)

class VirtualMachine:
    def __init__(self, code):
        self.code = code
        self.labels = {}
        self.instruction_pointer = 0

        self.rows = []
        self.row_cursor = -1
        self.current_row = None

        self.registers = []
        self.output = []
        self.current_table = None

        self._index_labels()

    def _index_labels(self):
        for idx, instruction in enumerate(self.code):
            if instruction[0] == Opcode.LABEL:
                self.labels[instruction[1]] = idx

    def run(self):
        while self.instruction_pointer < len(self.code):
            instr = self.code[self.instruction_pointer]
            opcode, *args = instr

            logger.debug(f"IP={self.instruction_pointer}: Executing {opcode.name} {args}")
            handler = getattr(self, f"op_{opcode.name.lower()}", None)
            if not handler:
                raise RuntimeError(f"No handler for opcode: {opcode.name}")
            handler(*args)

            if opcode not in {Opcode.JUMP, Opcode.JUMP_IF_FALSE}:
                self.instruction_pointer += 1

    def op_label(self, label_name):
        """
        Label marker - no operation at runtime.
        """
        logger.debug(f"LABEL: {label_name} (no-op)")
        pass
    
    def op_jump_if_false(self, label):
        """
        Pops a condition from the stack; jumps if condition is False.
        """
        condition = self.registers.pop()
        if not condition:
            self.instruction_pointer = self.labels[label]
            logger.debug(f"JUMP_IF_FALSE: Condition False -> Jump to {label}")
        else:
            self.instruction_pointer += 1
            logger.debug(f"JUMP_IF_FALSE: Condition True -> Continue")
    
    def op_jump(self, label):
        """
        Unconditionally jumps to the specified label.
        """
        self.instruction_pointer = self.labels[label]
        logger.debug(f"JUMP: Jump to {label}")
    
    def op_scan_end(self):
        """
        Marks end of table scan. No-op in memory model.
    """
        logger.debug("SCAN_END: Table scan complete.")


    def op_load_const(self, value):
        self.registers.append(value)
        logger.debug(f"LOAD_CONST: Pushed {value}")

    def op_open_table(self, table_name):
        self.current_table = table_name
        self.row_cursor = -1
        dummy_rows = {
            "users": [
                {"id": 1, "name": "Alice", "age": 30},
                {"id": 2, "name": "Bob", "age": 25},
                {"id": 3, "name": "Charlie", "age": 35}
            ],
            "orders": [
                {"id": 101, "user_id": 1, "amount": 250.0},
                {"id": 102, "user_id": 2, "amount": 150.0}
            ]
        }
        self.rows = dummy_rows.get(table_name, [])
        logger.debug(f"OPEN_TABLE: Loaded '{table_name}' with {len(self.rows)} rows.")

    def op_scan_start(self):
        self.row_cursor = -1
        logger.debug("SCAN_START: Cursor reset to beginning.")

    def op_scan_next(self):
        self.row_cursor += 1
        if self.row_cursor < len(self.rows):
            self.current_row = self.rows[self.row_cursor]
            self.registers.append(True)
            logger.debug(f"SCAN_NEXT: Row {self.row_cursor} = {self.current_row}")
        else:
            self.current_row = None
            self.registers.append(False)
            logger.debug("SCAN_NEXT: No more rows.")

    def op_load_column(self, column_name):
        if self.current_row is None:
            logger.error("LOAD_COLUMN with no current row.")
            raise RuntimeError("No current row to load column from.")
        value = self.current_row.get(column_name)
        self.registers.append(value)
        logger.debug(f"LOAD_COLUMN: {column_name} = {value}")

    def op_compare_eq(self):
        right = self.registers.pop()
        left = self.registers.pop()
        result = left == right
        self.registers.append(result)
        logger.debug(f"COMPARE_EQ: {left} == {right} -> {result}")

    def op_compare_neq(self):
        right = self.registers.pop()
        left = self.registers.pop()
        result = left != right
        self.registers.append(result)
        logger.debug(f"COMPARE_NEQ: {left} != {right} -> {result}")

    def op_compare_gt(self):
        right = self.registers.pop()
        left = self.registers.pop()
        result = left > right
        self.registers.append(result)
        logger.debug(f"COMPARE_GT: {left} > {right} -> {result}")

    def op_compare_lt(self):
        right = self.registers.pop()
        left = self.registers.pop()
        result = left < right
        self.registers.append(result)
        logger.debug(f"COMPARE_LT: {left} < {right} -> {result}")

    def op_compare_gte(self):
        right = self.registers.pop()
        left = self.registers.pop()
        result = left >= right
        self.registers.append(result)
        logger.debug(f"COMPARE_GTE: {left} >= {right} -> {result}")

    def op_compare_lte(self):
        right = self.registers.pop()
        left = self.registers.pop()
        result = left <= right
        self.registers.append(result)
        logger.debug(f"COMPARE_LTE: {left} <= {right} -> {result}")

    def op_emit_row(self, columns):
        if not self.current_row:
            logger.error("EMIT_ROW with no current row.")
            raise RuntimeError("No current row to emit.")
        result = {col: self.current_row.get(col) for col in columns}
        self.output.append(result)
        logger.info(f"EMIT_ROW: {result}")

    def op_insert_row(self, table):
        self.current_table = table
        logger.debug(f"INSERT_ROW: Preparing to insert into table '{self.current_table}'")
        
        table_schemas = {
            "users": ["name", "age"],
            "orders": ["id", "amount", "date"]
        }
        
        
        columns = table_schemas.get(self.current_table)
        if not columns:
            logger.error("INSERT_ROW with no open table.")
            raise RuntimeError(f"Unknown table schema for {self.current_table}")
        
        if len(self.registers) < len(columns):
            raise RuntimeError("Not enough values in registers for insert.")
        
        values = [self.registers.pop() for _ in range(len(columns))]
        values.reverse()
        row = dict(zip(columns, values))
        self.rows.append(row)
        
        logger.info(f"INSERT_ROW: Inserted into {self.current_table}: {row}")

    def op_update_column(self, column_name):
        if self.current_row is None:
            raise RuntimeError("No current row to update.")
        value = self.registers.pop()
        self.current_row[column_name] = value
        logger.debug(f"UPDATE_COLUMN: Set {column_name} = {value}")

    def op_update_row(self):
        if self.current_row is None:
            raise RuntimeError("No current row to commit update.")
        self.rows[self.row_cursor] = self.current_row.copy()
        logger.info(f"UPDATE_ROW: Row {self.row_cursor} updated: {self.current_row}")

    def op_delete_row(self):
        if self.current_row is None or self.row_cursor < 0:
            raise RuntimeError("No current row to delete.")
        deleted = self.rows.pop(self.row_cursor)
        logger.info(f"DELETE_ROW: Deleted row {self.row_cursor}: {deleted}")
        self.row_cursor -= 1
        self.current_row = None

    def op_create_table(self, table_name, columns):
        logger.info(f"CREATE_TABLE: Defined table '{table_name}' with columns: {columns}")

    def op_drop_table(self, table_name):
        logger.info(f"DROP_TABLE: Dropped table '{table_name}'")
