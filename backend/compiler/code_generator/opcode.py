from enum import Enum, auto
class Opcode(Enum):
    """
    This allows us to define a set of named constants for the various operations
    that can be performed by the query execution engine. Each operation corresponds
    to a specific action that the engine can take, such as manipulating data, 
    controlling flow, or performing comparisons.
    """
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
    INSERT_ROW = auto()        # Insert a new row into the table
    UPDATE_ROW = auto()        
    DELETE_ROW = auto()       # Delete the current row from the table
    UPDATE_COLUMN = auto()      # Update a column in the current row
    
    # Control Flow
    JUMP = auto()
    JUMP_IF_FALSE = auto()
    LABEL = auto()
    
    # Logical Operations
    LOGICAL_AND = auto()
    LOGICAL_OR = auto()
    LOGICAL_NOT = auto()
    
    # Comparison / Conditionals
    COMPARE_EQ = auto()
    COMPARE_NEQ = auto()
    COMPARE_LT = auto()
    COMPARE_LTE = auto()
    COMPARE_GT = auto()
    COMPARE_GTE = auto()
    
    # Output
    EMIT_ROW = auto()
    
    # Debug / Meta
    DEBUG_PRINT = auto()        # Print debug information
    HALT = auto()              # Halt execution