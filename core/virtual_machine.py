from compiler.code_generator.opcode import Opcode
from backend.table import Table
from utils.logger import get_logger
from backend.row_codec import encode_row, decode_row
from meta.catalog import Catalog

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
        self.catalog = Catalog()  # <-- Initialize Catalog

        self._index_labels()

    def _index_labels(self):
        self.labels = {}
        for idx, instruction in enumerate(self.code):
            if instruction[0].name == "LABEL":
                self.labels[instruction[1]] = idx

    def run(self):
        self.instruction_pointer = 0
        self._jumped = False
        while self.instruction_pointer < len(self.code):
            instr = self.code[self.instruction_pointer]
            op = instr[0]
            args = instr[1:]
            method = getattr(self, f"op_{op.name.lower()}", None)
            if method:
                logger.debug(f"IP={self.instruction_pointer}: Executing {op.name} {args}")
                method(*args)
                if hasattr(self, '_jumped') and self._jumped:
                    self._jumped = False
                    continue
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
            self._jumped = True
            logger.debug(f"JUMP_IF_FALSE: Jumping to {label}")
        else:
            logger.debug(f"JUMP_IF_FALSE: Condition true, not jumping.")
    
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
        self.row_metadata = {}
        for key, value in self.current_table.scan_page(self.current_table.root_page_num):
            try:
                row = decode_row(value)
            except Exception as e:
                logger.warning(f"Skipping corrupt or empty row: {e}")
                continue
            row["rowid"] = key
            self.rows.append(row)
            self.row_metadata[key] = (self.current_table.root_page_num, None)
        logger.info(f"OPEN_TABLE: Loaded {len(self.rows)} rows from table '{table_name}'")
        self.row_cursor = -1
        logger.debug(f"Rows loaded: {self.rows}")

    def op_scan_start(self):
        self.row_cursor = -1
        logger.debug("SCAN_START: Cursor reset to beginning.")

    def op_scan_next(self):
        self.row_cursor += 1
        if self.row_cursor < len(self.rows):
            self.current_row = self.rows[self.row_cursor]
            self.registers.append(True)
            logger.debug(f"SCAN_NEXT: Cursor at {self.row_cursor}, row: {self.current_row}")
        else:
            self.current_row = None
            self.registers.append(False)
            logger.debug(f"SCAN_NEXT: Cursor at {self.row_cursor}, end of rows.")

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
        if (isinstance(left, (int, float)) and isinstance(right, (int, float))) or (isinstance(left, str) and isinstance(right, str)):
            result = left > right
        else:
            logger.error(f"COMPARE_GT: Incompatible types for >: {type(left)} and {type(right)}")
            raise RuntimeError(f"Cannot compare {left} (type {type(left).__name__}) and {right} (type {type(right).__name__})")
        self.registers.append(result)
        logger.debug(f"COMPARE_GT: {left} > {right} -> {result}")

    def op_compare_lt(self):
        right = self.registers.pop()
        left = self.registers.pop()
        if (isinstance(left, (int, float)) and isinstance(right, (int, float))) or (isinstance(left, str) and isinstance(right, str)):
            result = left < right
        else:
            logger.error(f"COMPARE_LT: Incompatible types for <: {type(left)} and {type(right)}")
            raise RuntimeError(f"Cannot compare {left} (type {type(left).__name__}) and {right} (type {type(right).__name__})")
        self.registers.append(result)
        logger.debug(f"COMPARE_LT: {left} < {right} -> {result}")

    def op_compare_gte(self):
        right = self.registers.pop()
        left = self.registers.pop()
        if (isinstance(left, (int, float)) and isinstance(right, (int, float))) or (isinstance(left, str) and isinstance(right, str)):
            result = left >= right
        else:
            logger.error(f"COMPARE_GTE: Incompatible types for >=: {type(left)} and {type(right)}")
            raise RuntimeError(f"Cannot compare {left} (type {type(left).__name__}) and {right} (type {type(right).__name__})")
        self.registers.append(result)
        logger.debug(f"COMPARE_GTE: {left} >= {right} -> {result}")

    def op_compare_lte(self):
        right = self.registers.pop()
        left = self.registers.pop()
        if (isinstance(left, (int, float)) and isinstance(right, (int, float))) or (isinstance(left, str) and isinstance(right, str)):
            result = left <= right
        else:
            logger.error(f"COMPARE_LTE: Incompatible types for <=: {type(left)} and {type(right)}")
            raise RuntimeError(f"Cannot compare {left} (type {type(left).__name__}) and {right} (type {type(right).__name__})")
        self.registers.append(result)
        logger.debug(f"COMPARE_LTE: {left} <= {right} -> {result}")

    def op_emit_row(self, columns):
        if not self.current_row:
            logger.debug("EMIT_ROW: No current row to emit.")
            return
        result = {col: self.current_row.get(col) for col in columns}
        self.output.append(result)
        logger.info(f"EMIT_ROW: {result}")

    def op_insert_row(self, table):
        logger.debug(f"INSERT_ROW: Inserting into table '{table}'")
        self.current_table = Table(table)
        # Get schema from catalog
        schema_info = self.catalog.get_schema(table)
        if not schema_info:
            raise Exception(f"Table '{table}' does not exist in catalog.")
        columns = [col[0] for col in schema_info["columns"]]
        logger.debug(f"Register stack: {self.registers} (expecting {len(columns)} values)")
        if len(self.registers) < len(columns):
            raise Exception(f"Not enough values on stack for insert into '{table}'")
        # Extract values from stack in reverse order
        values = []
        for col in reversed(columns):
            values.append(self.registers.pop())
            logger.debug(f"Popped value for column '{col}': {values[-1]}")
        row = dict(zip(columns, values[::-1]))
        encoded = encode_row(row)
        # Determine a new row ID
        existing_page = self.current_table.load_root_page()
        max_id = max([key for key,_ in existing_page.cells], default=0)
        new_row_id = max_id + 1
        self.current_table.insert(new_row_id, encoded)
        self.current_table.save_root_page(existing_page)
        logger.info(f"INSERT_ROW: Inserted row with ID {new_row_id} into table '{table}'")
        row["rowid"] = new_row_id
        self.rows.append(row)
        self.current_table.close()
        self.current_table = None

    def op_update_column(self, column_name):
        if self.current_row is None:
            raise RuntimeError("No current row to update.")
        value = self.registers.pop()
        self.current_row[column_name] = value
        logger.debug(f"UPDATE_COLUMN: Set {column_name} = {value}")

    def op_update_row(self):
        if self.current_row is None:
            raise RuntimeError("No current row to commit update.")
        rowid = self.current_row["rowid"]
        page_num, _ = self.row_metadata[rowid]
        page = self.current_table.load_page(page_num)
        new_value = encode_row(self.current_row)
        page.update_leaf_cell(rowid, new_value)
        self.current_table.save_page(page_num, page)
        self.rows[self.row_cursor] = self.current_row.copy()
        logger.info(f"UPDATE_ROW: Row {self.row_cursor} updated and persisted: {self.current_row}")


    def op_delete_row(self):
        if self.current_row is None or self.row_cursor < 0:
            raise RuntimeError("No current row to delete.")
        rowid = self.current_row["rowid"]
        page_num, _ = self.row_metadata[rowid]
        page = self.current_table.load_page(page_num)
        page.delete_leaf_cell(rowid)
        self.current_table.save_page(page_num, page)
        del self.row_metadata[rowid]
        deleted_row = self.rows.pop(self.row_cursor)
        logger.info(f"DELETE_ROW: Deleted row {rowid}: {deleted_row}")
        self.row_cursor -= 1
        self.current_row = None

    def op_create_table(self, table_name, columns):
        # columns: list of (name, type) tuples
        logger.info(f"CREATE_TABLE: Defined table '{table_name}' with columns: {columns}")
        # Allocate a new table file and root page
        tbl = Table(table_name)
        root_page = tbl.root_page_num
        tbl.close()
        self.catalog.create_table(table_name, columns, root_page)

    def op_drop_table(self, table_name):
        logger.info(f"DROP_TABLE: Dropped table '{table_name}'")
        
    def op_logical_and(self):
        left = self.registers.pop()
        right = self.registers.pop()
        result = bool(left) and bool(right)
        self.registers.append(result)
        logger.debug(f"LOGICAL_AND: {left} AND {right} -> {result}")
        
    def op_logical_or(self):
        left = self.registers.pop()
        right = self.registers.pop()
        result = bool(left) or bool(right)
        self.registers.append(result)
        logger.debug(f"LOGICAL_OR: {left} OR {right} -> {result}")
        
    def op_logical_not(self):
        operand = self.registers.pop()
        result = not bool(operand)
        self.registers.append(result)
        logger.debug(f"LOGICAL_NOT: NOT {operand} -> {result}")
