from compiler.code_generator.create_codegen import CreateCodeGenerator
from compiler.code_generator.select_codegen import SelectCodeGenerator
from compiler.code_generator.insert_codegen import InsertCodeGenerator
from compiler.code_generator.update_codegen import UpdateCodeGenerator
from compiler.code_generator.delete_codegen import DeleteCodeGenerator
from compiler.code_generator.drop_codegen import DropCodeGenerator

from utils.logger import get_logger

logger = get_logger(__name__)

def generate(ast):
    logger.debug(f"Received AST for code generation: {ast}")
    stmt_type = ast["type"].upper()
    logger.info(f"Generating code for statement type: {stmt_type}")

    if stmt_type == "CREATE":
        logger.debug("Dispatching to CreateCodeGenerator")
        result = CreateCodeGenerator(ast).generate()
        logger.debug(f"Generated code for CREATE: {result}")
        return result
    elif stmt_type == "SELECT":
        logger.debug("Dispatching to SelectCodeGenerator")
        result = SelectCodeGenerator(ast).generate()
        logger.debug(f"Generated code for SELECT: {result}")
        return result
    elif stmt_type == "INSERT":
        logger.debug("Dispatching to InsertCodeGenerator")
        result = InsertCodeGenerator(ast).generate()
        logger.debug(f"Generated code for INSERT: {result}")
        return result
    elif stmt_type == "UPDATE":
        logger.debug("Dispatching to UpdateCodeGenerator")
        result = UpdateCodeGenerator(ast).generate()
        logger.debug(f"Generated code for UPDATE: {result}")
        return result
    elif stmt_type == "DELETE":
        logger.debug("Dispatching to DeleteCodeGenerator")
        result = DeleteCodeGenerator(ast).generate()
        logger.debug(f"Generated code for DELETE: {result}")
        return result
    elif stmt_type == "DROP":
        logger.debug("Dispatching to DropCodeGenerator")
        result = DropCodeGenerator(ast).generate()
        logger.debug(f"Generated code for DROP: {result}")
        return result
    else:
        logger.error(f"Unsupported statement type: {stmt_type}")
        raise NotImplementedError(f"Code generation for {stmt_type} statements is not implemented yet.")