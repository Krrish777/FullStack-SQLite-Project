from compiler.code_generator.base_codegen import BaseCodeGenerator
from compiler.code_generator.opcode import Opcode

class InsertCodeGenerator(BaseCodeGenerator):
    def generate(self):
        table = self.ast["table"]
        values = self.ast["values"]
        
        code = []
        
        for value in values:
            code.append((Opcode.LOAD_CONST, value))
            
        code.append((Opcode.INSERT_ROW, table))
        
        return code