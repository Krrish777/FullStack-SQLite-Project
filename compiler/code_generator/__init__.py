from compiler.code_generator.create_codegen import CreateCodeGenerator
from compiler.code_generator.select_codegen import SelectCodeGenerator
from compiler.code_generator.insert_codegen import InsertCodeGenerator
from compiler.code_generator.update_codegen import UpdateCodeGenerator
from compiler.code_generator.delete_codegen import DeleteCodeGenerator
from compiler.code_generator.drop_codegen import DropCodeGenerator

from utils.logger import get_logger

logger = get_logger(__name__)

def generate(ast):
    stmt_type = ast["type"].upper()
    
    if stmt_type == "CREATE":
        return CreateCodeGenerator(ast).generate()
    elif stmt_type == "SELECT":
        return SelectCodeGenerator(ast).generate()
    elif stmt_type == "INSERT":
        return InsertCodeGenerator(ast).generate()
    elif stmt_type == "UPDATE":
        return UpdateCodeGenerator(ast).generate()
    elif stmt_type == "DELETE":
        return DeleteCodeGenerator(ast).generate()
    elif stmt_type == "DROP":
        return DropCodeGenerator(ast).generate()
    else:
        logger.error(f"Unsupported statement type: {stmt_type}")
        raise NotImplementedError(f"Code generation for {stmt_type} statements is not implemented yet.")