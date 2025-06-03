from compiler.code_generator.base_codegen import BaseCodeGenerator
from compiler.code_generator.opcode import Opcode

class DeleteCodeGenerator(BaseCodeGenerator):
    def generate(self):
        table = self.ast["table"]
        where = self.ast.get("where", None)
        
        loop_label = self.new_label()
        end_label = self.new_label()
        skip_label = self.new_label()
        
        code = [
            (Opcode.OPEN_TABLE, table),
            (Opcode.SCAN_START,),
            (Opcode.LABEL, loop_label),
            (Opcode.SCAN_NEXT,),
            (Opcode.JUMP_IF_FALSE, end_label)
        ]

        if where:
            code += [
                (Opcode.LOAD_COLUMN, where["column"]),
                (Opcode.LOAD_CONST, where["value"]),
                (self._get_comparison_opcode(where["operator"]),),
                (Opcode.JUMP_IF_FALSE, skip_label)
            ]

        code.append((Opcode.DELETE_ROW,))

        if where:
            code.append((Opcode.LABEL, skip_label))

        code += [
            (Opcode.JUMP, loop_label),
            (Opcode.LABEL, end_label),
            (Opcode.SCAN_END,)
        ]

        return code

    def _get_comparison_opcode(self, operator):
        return {
            "=": Opcode.COMPARE_EQ,
            "==": Opcode.COMPARE_EQ,
            "!=": Opcode.COMPARE_NEQ,
            "<": Opcode.COMPARE_LT,
            "<=": Opcode.COMPARE_LTE,
            ">": Opcode.COMPARE_GT,
            ">=": Opcode.COMPARE_GTE,
        }.get(operator) or ValueError(f"Unsupported operator: {operator}")