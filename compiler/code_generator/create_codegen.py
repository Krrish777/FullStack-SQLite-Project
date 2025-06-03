from compiler.code_generator.base_codegen import BaseCodeGenerator
from compiler.code_generator.opcode import Opcode

class CreateCodeGenerator(BaseCodeGenerator):
    def generate(self):
        table_name = self.ast["table_name"]
        columns = self.ast["columns"]
        
        return [
            (Opcode.CREATE_TABLE, table_name, columns)
        ]