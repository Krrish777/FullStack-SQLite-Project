# 🔧 SQLite-Like Database Engine in Python

This is a **modular, compiler-based educational database engine** built from scratch in Python, inspired by SQLite. The project follows a layered architecture with distinct components for tokenization, parsing, code generation, and virtual machine execution.

> 🎯 Goal: To understand and recreate the core internals of a relational database engine using compiler and systems programming principles.

---

## ✅ Features Implemented

- **Tokenizer**: Converts raw SQL into structured tokens
- **Parser**: Builds abstract syntax trees (ASTs) from token streams
- **Code Generator**: Transforms ASTs into low-level bytecode-like opcodes
- **Opcode Design**: Custom instruction set for SQL-like operations
- **CLI Testing**: Run SQL queries directly via command line

---

## 🧱 Architecture Overview

```
SQL Query
   ↓
Tokenizer
   ↓
Parser
   ↓
AST
   ↓
Code Generator
   ↓
Opcodes (Bytecode)
   ↓
Virtual Machine (coming soon!)
   ↓
Result Rows
```

---

## 🗂️ Project Structure

```
.
├── compiler/
│   ├── tokenizer/
|   ├── __init__.py
|   ├── token_definitions.py
|   ├── tokenizer.py
│   ├── parser/
|   ├── __init.py
|   ├── parser.py
|   ├── statements.py
│   ├── code_generator/
|   ├── __init__.py
|   ├── base_codege.py
|   ├── create_codege.py
|   ├── delete_codege.py
|   ├── drop_codege.py
|   ├── insert_codege.py
|   ├── select_codege.py
|   ├── update_codege.py
│   └── opcode.py
├── core/
|   ├── __init__.py
│   └── virtual_machine.py   # (In Progress)
├── backend/                 # (Planned)
|   ├── __init__.py
│   ├── btree.py
│   ├── pager.py
│   └── os_interface.py
├── utils/
|   ├── __init__.py
│   ├── logger.py
│   └── errors.py
├── requirements.txt 
├── main.py
├── test.sh
└── README.md
```

---

## 🚀 Running the Project

### 💻 Run a SQL Query

```bash
python3 main.py "SELECT * FROM users WHERE age > 30;"
```

### 🧪 Run All Tests

```bash
bash test.sh
```

Output will include parsed ASTs and opcode execution plans.

---

## 🔨 Current SQL Support

- `CREATE TABLE`
- `INSERT INTO ... VALUES`
- `SELECT ... FROM ... [WHERE]`
- `UPDATE ... SET ... [WHERE]`
- `DELETE FROM ... [WHERE]`
- `DROP TABLE`

---

## 🔄 Next Steps

- [x] Full code generator with opcode dispatch
- [ ] Virtual machine execution loop
- [ ] Row storage engine (B-Tree)
- [ ] File-backed storage and pager
- [ ] Type checking and schema validation
- [ ] Subqueries, joins, and more

---

## 🧠 Learning Focus

This project is built with a **"Build Your Own X"** learning mindset. Key topics explored include:

- Compiler internals (tokenizer, parser, codegen)
- Stack-based virtual machines
- SQL grammar and execution logic
- Modular system design
- Clean logging, CLI output, and test automation

---

## 🤝 Contributors

Built by Krish Sharma — feel free to fork, study, and contribute!

---

## 📘 License

This project is open-source and available under the MIT License.