from compiler.code_generator.opcode import Opcode
from backend.table import Table
from utils.logger import get_logger
from backend.row_codec import encode_row, decode_row

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
        logger.debug(f"OPEN_TABLE: Opening table '{table_name}'")
        self.current_table = Table(table_name)
        self.rows = []
        
        page = self.current_table.load_root_page()
        
        for key, value in page.cells:
            try:
                row = decode_row(value)
            except Exception as e:
                logger.warning(f"Skipping corrupt or empty row: {e}")
                continue
            row["rowid"] = key
            self.rows.append(row)
            
        logger.info(f"OPEN_TABLE: Loaded {len(self.rows)} rows from table '{table_name}'")
        self.row_cursor = -1       

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
        left = self.registers.pop()
        right = self.registers.pop()
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
        logger.debug(f"INSERT_ROW: Inserting into table '{table}'")
        self.current_table = Table(table)
        
        table_schema = {
            "users": ["name", "age"],
            "orders": ["id", "amount", "date"]
        }
        
        columns = table_schema.get(table)
        if not columns:
            raise RuntimeError(f"Table '{table}' not found in schema.")
        
        logger.debug(f"Register stack: {self.registers} (expecting {len(columns)} values)")
        
        if len(self.registers) < len(columns):
            raise RuntimeError("Not enough values in registers to insert row.")
        
        # Extract values from stack in reverse order
        values = [self.registers.pop() for _ in columns]
        values.reverse() # to match column order
        
        row = dict(zip(columns, values))
        encoded = encode_row(row)
        
        # Determine a new row ID
        existing_page = self.current_table.load_root_page()
        max_id = max([key for key,_ in existing_page.cells], default=0)
        new_row_id = max_id + 1
        
        existing_page.add_leaf_cell(new_row_id, encoded)
        self.current_table.save_root_page(existing_page)
        
        logger.info(f"INSERT_ROW: Inserted row with ID {new_row_id} into table '{table}'")
        row["rowid"] = new_row_id
        self.rows.append(row)

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
