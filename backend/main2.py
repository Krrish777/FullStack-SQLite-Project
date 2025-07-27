import sys
import os
import shutil
from typing import Optional, Any, Dict, List
import time
import json

# FastAPI imports
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Your existing imports
from compiler.tokenizer import Tokenizer
from compiler.parser.statements import parse_statement
from compiler.parser import Parser
from compiler.code_generator import generate
from core.virtual_machine import VirtualMachine
from utils.errors import TokenizationError
from utils.logger import get_logger

# FastAPI app instance
app = FastAPI(
    title="SQLite Clone API",
    description="SQLite-like Database Engine API",
    version="0.1.0"
)

# Update your CORS configuration in your FastAPI file
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://127.0.0.1:5173"],  # Add Vite default ports
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Constants
DATABASES_ROOT = os.path.join(os.path.dirname(__file__), "database")
current_db = "main"  # Default database

# Pydantic models
class SQLRequest(BaseModel):
    query: str
    database: Optional[str] = "main"

class SQLResponse(BaseModel):
    success: bool
    query: str
    database: str
    execution_time_ms: float
    tokens: Optional[List[Dict[str, str]]] = None
    parse_tree: Optional[Dict[str, Any]] = None
    opcodes: Optional[List[str]] = None
    result: Optional[List[Any]] = None
    message: Optional[str] = None
    error: Optional[str] = None

class DatabaseInfo(BaseModel):
    name: str
    tables: List[str]

class TableInfo(BaseModel):
    name: str
    exists: bool
    
class DatabaseCreateRequest(BaseModel):
    name: str

# Utility functions (converted from your existing code)
def get_db_path(db_name):
    return os.path.join(DATABASES_ROOT, db_name)

def ensure_databases_root():
    os.makedirs(DATABASES_ROOT, exist_ok=True)

def create_database_internal(name: str):
    ensure_databases_root()
    db_path = get_db_path(name)
    if os.path.exists(db_path):
        return False, f"Database '{name}' already exists."
    os.makedirs(db_path)
    open(os.path.join(db_path, "__catalog.tbl"), "wb").close()
    return True, f"Database '{name}' created."

def delete_database_internal(name: str):
    db_path = get_db_path(name)
    if not os.path.exists(db_path):
        return False, f"Database '{name}' does not exist."
    shutil.rmtree(db_path)
    return True, f"Database '{name}' deleted."

def list_databases_internal():
    ensure_databases_root()
    dbs = [d for d in os.listdir(DATABASES_ROOT) if os.path.isdir(get_db_path(d))]
    return dbs

def list_tables_internal(db_name: str):
    db_path = get_db_path(db_name)
    if not os.path.exists(db_path):
        return []
    tbls = [f[:-4] for f in os.listdir(db_path) if f.endswith('.tbl') and f != "__catalog.tbl"]
    return tbls

def process_sql_internal(sql: str, db_name: str):
    """Process SQL query and return structured response"""
    db_path = get_db_path(db_name)
    if not os.path.exists(db_path):
        raise Exception(f"Database '{db_name}' does not exist.")
    
    logger = get_logger(__name__)
    tokenizer = Tokenizer()
    
    try:
        # Tokenization
        tokens = tokenizer.tokenize(sql)
        token_list = [{"type": str(token_type), "value": str(token_value)} for token_type, token_value in tokens]
        
        # Parsing
        parser = Parser(tokens)
        parse_tree = parse_statement(parser)
        
        # Code generation
        codegen = generate(parse_tree)
        opcode_list = []
        for opcode, *args in codegen:
            args_str = ", ".join(map(str, args))
            opcode_list.append(f"{opcode.name}({args_str})")
        
        # Virtual machine execution
        vm = VirtualMachine(codegen, db_path=db_path)
        vm.run()
        
        # Format result
        result = None
        message = None
        
        if vm.output:
            result = vm.output
        elif parse_tree.get("type") == "INSERT":
            message = "Insert operation completed successfully."
        elif parse_tree.get("type") == "CREATE":
            message = "Table created successfully."
        elif parse_tree.get("type") == "DROP":
            message = "Table dropped successfully."
        elif parse_tree.get("type") == "UPDATE":
            message = "Update operation completed successfully."
        elif parse_tree.get("type") == "DELETE":
            message = "Delete operation completed successfully."
        
        return {
            "success": True,
            "tokens": token_list,
            "parse_tree": parse_tree,
            "opcodes": opcode_list,
            "result": result,
            "message": message,
            "error": None
        }
        
    except TokenizationError as e:
        logger.error(f"Tokenization error: {e}")
        return {
            "success": False,
            "tokens": None,
            "parse_tree": None,
            "opcodes": None,
            "result": None,
            "message": None,
            "error": f"Tokenization error: {str(e)}"
        }
    except SyntaxError as e:
        logger.error(f"Syntax error: {e}")
        return {
            "success": False,
            "tokens": None,
            "parse_tree": None,
            "opcodes": None,
            "result": None,
            "message": None,
            "error": f"Syntax error: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {
            "success": False,
            "tokens": None,
            "parse_tree": None,
            "opcodes": None,
            "result": None,
            "message": None,
            "error": f"Unexpected error: {str(e)}"
        }

# FastAPI Routes
@app.get("/")
async def root():
    return {
        "message": "SQLite Clone API is running!",
        "version": "0.1.0",
        "author": "Krish Sharma",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/demo/query", response_model=SQLResponse)
async def execute_query(request: SQLRequest):
    """Execute SQL query using the database engine"""
    start_time = time.time()
    
    try:
        # Process the SQL query
        result = process_sql_internal(request.query, request.database)
        execution_time = (time.time() - start_time) * 1000
        
        return SQLResponse(
            success=result["success"],
            query=request.query,
            database=request.database,
            execution_time_ms=execution_time,
            tokens=result["tokens"],
            parse_tree=result["parse_tree"],
            opcodes=result["opcodes"],
            result=result["result"],
            message=result["message"],
            error=result["error"]
        )
        
    except Exception as e:
        execution_time = (time.time() - start_time) * 1000
        return SQLResponse(
            success=False,
            query=request.query,
            database=request.database,
            execution_time_ms=execution_time,
            error=str(e)
        )

@app.get("/demo/databases")
async def list_databases():
    """List all available databases"""
    try:
        databases = list_databases_internal()
        db_info = []
        for db_name in databases:
            tables = list_tables_internal(db_name)
            db_info.append(DatabaseInfo(name=db_name, tables=tables))
        
        return {"databases": db_info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/demo/databases/{database_name}/tables")
async def list_tables(database_name: str):
    """List all tables in a specific database"""
    try:
        tables = list_tables_internal(database_name)
        return {"database": database_name, "tables": tables}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/demo/databases")
async def create_database(request: DatabaseCreateRequest):
    """Create a new database"""
    try:
        success, message = create_database_internal(request.name)
        if success:
            return {"success": True, "message": message}
        else:
            raise HTTPException(status_code=400, detail=message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/demo/databases/{database_name}")
async def delete_database(database_name: str):
    """Delete a database and all its tables"""
    try:
        success, message = delete_database_internal(database_name)
        if success:
            return {"success": True, "message": message}
        else:
            raise HTTPException(status_code=404, detail=message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/demo/tables/{table_name}/info")
async def get_table_info(table_name: str, database: str = "main"):
    """Get information about a specific table"""
    try:
        tables = list_tables_internal(database)
        exists = table_name in tables
        return TableInfo(name=table_name, exists=exists)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Initialize database directory on startup
@app.on_event("startup")
async def startup_event():
    ensure_databases_root()
    # Create default database if it doesn't exist
    if not os.path.exists(get_db_path("main")):
        create_database_internal("main")

# Run the server
if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting SQLite Clone API Server...")
    print("📖 API Docs: http://localhost:8000/docs")
    print("🔗 Demo Endpoints: http://localhost:8000/demo/")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )