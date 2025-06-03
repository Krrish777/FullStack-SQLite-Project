from compiler.code_generator.create_codegen import CreateCodeGenerator

def generate(ast):
    stmt_type = ast["type"]
    
    if stmt_type == "CREATE":
        return CreateCodeGenerator(ast).generate()
    raise NotImplementedError(f"Code generation for {stmt_type} statements is not implemented yet.")