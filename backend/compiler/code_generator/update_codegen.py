from compiler.code_generator.base_codegen import BaseCodeGenerator
from compiler.code_generator.opcode import Opcode
from utils.logger import get_logger

logger = get_logger(__name__)

class UpdateCodeGenerator(BaseCodeGenerator):
    def generate(self):
        logger.info("Generating UPDATE code")
        table = self.ast["table"]
        set_clauses = self.ast["set"]
        where = self.ast.get("where", None)

        loop_label = self.new_label("loop")
        end_label = self.new_label("end")
        skip_label = self.new_label("skip") if where else None

        code = [
            (Opcode.OPEN_TABLE, table),
            (Opcode.SCAN_START,),
            (Opcode.LABEL, loop_label),
            (Opcode.SCAN_NEXT,),
            (Opcode.JUMP_IF_FALSE, end_label)
        ]

        if where:
            if isinstance(where, list):
                for idx, cond in enumerate(where):
                    code.append((Opcode.LOAD_COLUMN, cond["column"]))
                    code.append((Opcode.LOAD_CONST, cond["value"]))
                    code.append((self._get_comparison_opcode(cond["operator"]),))
                    if idx > 0:
                        code.append((Opcode.LOGICAL_AND,))
                code.append((Opcode.JUMP_IF_FALSE, skip_label))
            else:
                code += [
                    (Opcode.LOAD_COLUMN, where["column"]),
                    (Opcode.LOAD_CONST, where["value"]),
                    (self._get_comparison_opcode(where["operator"]),),
                    (Opcode.JUMP_IF_FALSE, skip_label)
                ]

        # SET clauses
        for col, val in set_clauses:
            code.append((Opcode.LOAD_CONST, val))
            code.append((Opcode.UPDATE_COLUMN, col))
        code.append((Opcode.UPDATE_ROW,))

        if where:
            code.append((Opcode.LABEL, skip_label))

        code += [
            (Opcode.JUMP, loop_label),
            (Opcode.LABEL, end_label),
            (Opcode.SCAN_END,)
        ]
        logger.debug(f"Generated UPDATE code: {code}")
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