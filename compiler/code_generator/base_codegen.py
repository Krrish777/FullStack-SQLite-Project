from abc import ABC, abstractmethod
from compiler.code_generator.opcode import Opcode

class BaseCodeGenerator(ABC):
    """
    Abstract base class for all SQL code generators.
    """
    def __init__(self, ast):
        self.ast = ast
        self.label_counter = 0
        
    def new_label(self, prefix="label"):
        self.label_counter += 1
        return f"{prefix}_{self.label_counter}"
        
    @abstractmethod # This method must be implemented by subclasses
    def generate(self):
        """
        Returns a list of Opcodes that represent the SQL code generated from the AST.
        """
        pass