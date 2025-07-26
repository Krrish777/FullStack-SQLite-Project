# 🔧 SQLite-Like Database Engine in Python

This is a **complete, modular, compiler-based educational database engine** built from scratch in Python, inspired by SQLite. The project follows a layered architecture with distinct components for tokenization, parsing, code generation, virtual machine execution, and persistent storage.

> 🎯 **Goal**: To understand and recreate the core internals of a relational database engine using compiler and systems programming principles.

🚀 **Project Status**: **COMPLETE** ✅ - Full working database engine with persistent storage!

---

## ✅ Features Implemented

### 🧠 **Compiler Frontend**
- **Tokenizer**: Converts raw SQL into structured tokens (`compiler/tokenizer/`)
- **Parser**: Builds abstract syntax trees (ASTs) from token streams (`compiler/parser/`)
- **Code Generator**: Transforms ASTs into low-level opcodes/bytecode (`compiler/code_generator/`)
- **Opcode Design**: Custom instruction set for SQL-like operations (`compiler/code_generator/opcode.py`)

### ⚙️ **Execution Engine**
- **Virtual Machine**: Complete execution engine for opcodes (`core/virtual_machine.py`) ✅
- **Database Session**: Query processing and transaction management (`core/database_session.py`) ✅
- **SQL Processor**: High-level SQL query coordination (`core/sql_processor.py`) ✅

### 💾 **Storage Backend**
- **B-Tree**: Complete row storage and indexing implementation (`backend/btree.py`) ✅
- **Pager**: Database file paging and caching system (`backend/pager.py`) ✅
- **OS Interface**: File system operations for persistence (`backend/os_interface.py`) ✅
- **Row Codec**: Row encoding/decoding with type support (`backend/row_codec.py`) ✅
- **Table Management**: Complete table abstraction layer (`backend/table.py`) ✅

### 📊 **Schema & Metadata**
- **Catalog Management**: Complete schema and metadata management (`meta/catalog.py`) ✅
- **Database Files**: Persistent database storage in `database/` directory ✅

### 🛠️ **Utilities & Infrastructure**
- **Logging System**: Structured logging and error reporting (`utils/logger.py`, `logs/`) ✅
- **Error Handling**: Comprehensive error management (`utils/errors.py`) ✅
- **Validation**: Input and schema validation (`utils/validation.py`) ✅
- **Pretty Printing**: Formatted output display (`utils/pretty_printer.py`) ✅
- **CLI Interface**: Full command-line interface (`main.py`) ✅

---

## 🧱 Architecture Overview

```
SQL Query
   ↓
🔤 Tokenizer (Lexical Analysis)
   ↓
🌳 Parser (Syntax Analysis) 
   ↓
📋 AST (Abstract Syntax Tree)
   ↓
⚡ Code Generator (Bytecode Generation)
   ↓
🔧 Opcodes (Virtual Machine Instructions)
   ↓
🖥️  Virtual Machine (Execution Engine)
   ↓
💾 Storage Backend (B-Tree + Pager)
   ↓
📊 Result Rows
```

### 🎯 **Key Design Principles**
- **Compiler-based**: Traditional compiler phases (lexing, parsing, codegen, execution)
- **Stack-based VM**: Bytecode execution with operand stack
- **B-Tree Storage**: Efficient row storage and retrieval
- **Page-based I/O**: Database file management with caching
- **Modular Design**: Clean separation of concerns

---

## 🗂️ Project Structure

```
.
├── compiler/                    # 🧠 Frontend Compilation
│   ├── tokenizer/              #    Lexical Analysis
│   │   ├── __init__.py
│   │   ├── token_definitions.py
│   │   └── tokenizer.py
│   ├── parser/                 #    Syntax Analysis  
│   │   ├── __init__.py
│   │   ├── parser.py
│   │   └── statements.py
│   └── code_generator/         #    Bytecode Generation
│       ├── __init__.py
│       ├── base_codegen.py
│       ├── create_codegen.py
│       ├── delete_codegen.py
│       ├── drop_codegen.py
│       ├── insert_codegen.py
│       ├── select_codegen.py
│       ├── update_codegen.py
│       └── opcode.py
├── core/                       # ⚙️ Execution Engine
│   ├── __init__.py
│   ├── database_session.py     #    Session Management
│   ├── sql_processor.py        #    Query Coordination
│   └── virtual_machine.py      #    Bytecode Execution ✅
├── backend/                    # 💾 Storage Engine
│   ├── __init__.py
│   ├── btree.py               #    B-Tree Implementation ✅
│   ├── pager.py               #    Page Management ✅
│   ├── os_interface.py        #    File I/O Operations ✅
│   ├── row_codec.py           #    Row Serialization ✅
│   └── table.py               #    Table Abstraction ✅
├── meta/                      # 📊 Schema Management
│   ├── __init__.py
│   └── catalog.py             #    Metadata & Catalog ✅
├── utils/                     # 🛠️ Utilities
│   ├── __init__.py
│   ├── errors.py              #    Error Handling ✅
│   ├── logger.py              #    Logging System ✅
│   ├── pretty_printer.py      #    Output Formatting ✅
│   └── validation.py          #    Input Validation ✅
├── database/                  # 💽 Persistent Storage
│   ├── mydb/                  #    Example Database
│   │   ├── __catalog.tbl      #    Schema Metadata
│   │   └── users.tbl          #    User Data
│   ├── testdb/                #    Test Database
│   │   ├── __catalog.tbl
│   │   └── logs.tbl
│   └── [other databases...]
├── logs/                      # 📝 Application Logs
│   ├── errors.log
│   ├── sqlite_clone.log
│   └── structured.jsonl
├── main.py                    # 🚀 CLI Entry Point
├── testcase.txt              # 🧪 Test Cases
├── requirements.txt          # 📦 Dependencies
└── README.md                 # 📚 Documentation
```

---

## 🚀 Running the Project

### 💻 **Execute SQL Queries**

```bash
# Run a single SQL query
python main.py "CREATE TABLE users (id INTEGER, name TEXT, age INTEGER);"
python main.py "INSERT INTO users VALUES (1, 'Alice', 25);"
python main.py "SELECT * FROM users WHERE age > 20;"
```

### 🪟 **Windows PowerShell**
```powershell
python main.py "SELECT * FROM users WHERE age > 30;"
```

### 🧪 **Run Test Suite**
```bash
# Execute all test cases
python main.py testcase.txt
```

### 📊 **View Execution Details**
The engine provides detailed output including:
- **Tokenization**: SQL tokens generated
- **AST**: Abstract syntax tree structure  
- **Bytecode**: Generated opcodes
- **Execution**: Step-by-step VM execution
- **Results**: Formatted query results

---

## 🔨 **Complete SQL Support**

### ✅ **Fully Implemented**
- **`CREATE TABLE`** - Table creation with column definitions
- **`INSERT INTO ... VALUES`** - Row insertion with type validation
- **`SELECT ... FROM ... [WHERE]`** - Query with filtering conditions
- **`UPDATE ... SET ... [WHERE]`** - Row updates with conditions
- **`DELETE FROM ... [WHERE]`** - Row deletion with conditions  
- **`DROP TABLE`** - Table removal

### 🎯 **Advanced Features**
- **Persistent Storage**: All data persisted to disk via B-Tree
- **Type System**: INTEGER, TEXT, REAL data types
- **WHERE Clauses**: Complex filtering conditions
- **Schema Validation**: Column type checking and constraints
- **Transaction Safety**: Consistent database state
- **Error Recovery**: Comprehensive error handling

---

## 🏗️ **Technical Implementation**

### 🧠 **Virtual Machine**
- **Stack-based execution**: Operand stack for expression evaluation
- **Opcode dispatch**: Custom instruction set for SQL operations
- **Memory management**: Efficient row and page caching
- **Error handling**: Graceful failure recovery

### 💾 **Storage Engine**
- **B-Tree structure**: Balanced tree for efficient storage/retrieval
- **Page-based I/O**: Fixed-size pages with LRU caching
- **Row serialization**: Compact binary encoding
- **File persistence**: Atomic writes and crash safety

### 📊 **Schema System**
- **Catalog tables**: Metadata storage in `__catalog.tbl`
- **Type validation**: Runtime type checking
- **Column constraints**: NOT NULL, type validation
- **Schema versioning**: Backward compatibility support

---

## 📈 **Performance Features**

- **B-Tree indexing**: O(log n) row access
- **Page caching**: Reduced disk I/O via LRU cache
- **Bytecode optimization**: Efficient VM instruction set
- **Lazy loading**: On-demand page loading
- **Compact storage**: Efficient row serialization

---

## 🎓 **Learning Outcomes**

This project demonstrates mastery of:

### 🔧 **Systems Programming**
- File I/O and page management
- Memory management and caching
- Binary data serialization
- Error handling and recovery

### 🧠 **Compiler Design**
- Lexical analysis and tokenization
- Recursive descent parsing
- Abstract syntax trees
- Code generation and optimization
- Virtual machine design

### 💾 **Database Internals**
- B-Tree data structures
- Query execution planning
- Schema and metadata management
- ACID properties implementation
- Storage engine architecture

### 🏗️ **Software Architecture**
- Modular system design
- Clean interfaces and abstraction
- Separation of concerns
- Comprehensive testing
- Documentation and logging

---

## 🎥 **Reference Videos**

This implementation was inspired by these excellent database internals videos:
- [Database Internals Deep Dive](https://youtu.be/IrzF4r9hqlY?si=4C14LVVD0mUfs3N5)
- [Building a Database Engine](https://youtu.be/hfbZqPpNiSM?si=ubDF4VwpW-q4FqFJ)

---

## 🔬 **Example Usage**

```sql
-- Create a table
CREATE TABLE employees (id INTEGER, name TEXT, salary INTEGER);

-- Insert data
INSERT INTO employees VALUES (1, 'John Doe', 50000);
INSERT INTO employees VALUES (2, 'Jane Smith', 60000);

-- Query data
SELECT * FROM employees WHERE salary > 55000;

-- Update records
UPDATE employees SET salary = 65000 WHERE name = 'Jane Smith';

-- Delete records
DELETE FROM employees WHERE id = 1;

-- Drop table
DROP TABLE employees;
```

---

## 🤝 **Contributing**

This project serves as an educational resource for understanding database internals. Feel free to:

- 🔀 **Fork** the repository
- 📖 **Study** the implementation
- 🐛 **Report** issues or improvements
- 💡 **Suggest** new features
- 📚 **Learn** from the codebase

---

## 👨‍💻 **Author**

**Built by Krish Sharma** 

A passionate developer exploring the depths of systems programming and database internals.

🔗 **Repository**: [github.com/Krrish777/Sqlite_Python](https://github.com/Krrish777/Sqlite_Python)

---

## 📄 **License**

This project is open-source and available under the **MIT License**.

---

## 🎉 **Project Status: COMPLETE!**

This SQLite-like database engine is fully functional with:
- ✅ Complete SQL query support
- ✅ Persistent storage via B-Tree
- ✅ Virtual machine execution
- ✅ Comprehensive error handling
- ✅ Production-ready architecture

Ready for educational use, further development, and learning database internals! 🚀