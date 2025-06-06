from compiler.code_generator.base_codegen import BaseCodeGenerator
from compiler.code_generator.opcode import Opcode
from utils.logger import get_logger

logger = get_logger(__name__)

class CreateCodeGenerator(BaseCodeGenerator):
    def generate(self):
        logger.info("Generating CREATE TABLE code")
        table = self.ast["table"]
        columns = self.ast["columns"]
        
        logger.debug(f"Generating CREATE TABLE code for table: {table} with columns: {columns}")
        return [
            (Opcode.CREATE_TABLE, table, columns)
        ]