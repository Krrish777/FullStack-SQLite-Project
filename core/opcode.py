from enum import Enum, auto
class Opcode(Enum):
    # Table & Schema Operations
    CREATE_TABLE = auto()
    DROP_TABLE = auto()
    OPEN_TABLE = auto()
    
    # Scanning
    SCAN_START = auto()
    SCAN_NEXT = auto()
    SCAN_END = auto()
    
    # Data Manipulation
    LOAD_CONST = auto()         # Push a constant onto the stack
    LOAD_COLUMN = auto()        # Load a column from the current row
    INSERT_ROW = auto()         # Insert a new row into the table
    DELETE_ROW = auto()         # Delete the current row from the table
    UPDATE_COLUMN = auto()      # Update a column in the current row
    
    # Control Flow
    JUMP = auto()
    JUMP_IF_FALSE = auto()
    LABEL = auto()
    
    # Comparison / Conditionals
    COMPARE_EQ = auto()
    COMPARE_LT = auto()
    COMPARE_GT = auto()
    
    # Output
    EMIT_ROW = auto()
    
    # Debug / Meta
    DEBUG_PRINT = auto()        # Print debug information
    HALT = auto()              # Halt execution