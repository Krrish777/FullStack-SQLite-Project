from compiler.code_generator.base_codegen import BaseCodeGenerator
from compiler.code_generator.opcode import Opcode

class DropCodeGenerator(BaseCodeGenerator):
    def generate(self):
        table = self.ast["table_name"]
        
        return [
            (Opcode.DROP_TABLE, table)
        ]