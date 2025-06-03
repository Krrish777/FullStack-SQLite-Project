from compiler.code_generator.create_codegen import CreateCodeGenerator
from compiler.code_generator.select_codegen import SelectCodeGenerator

def generate(ast):
    stmt_type = ast["type"]
    
    if stmt_type == "CREATE":
        return CreateCodeGenerator(ast).generate()
    raise NotImplementedError(f"Code generation for {stmt_type} statements is not implemented yet.")
    if stmt_type == "SELECT":
        return SelectCodeGenerator(ast).generate()
    raise NotImplementedError(f"Code generation for {stmt_type} statements is not implemented yet.")