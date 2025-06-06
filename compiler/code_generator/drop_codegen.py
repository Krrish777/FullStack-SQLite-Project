from compiler.code_generator.base_codegen import BaseCodeGenerator
from compiler.code_generator.opcode import Opcode
from utils.logger import get_logger

logger = get_logger(__name__)

class DropCodeGenerator(BaseCodeGenerator):
    def generate(self):
        logger.info("Generating DROP TABLE code")
        table = self.ast["table"]
        
        logger.debug(f"Generating DROP TABLE code for table: {table}")
        return [
            (Opcode.DROP_TABLE, table)
        ]