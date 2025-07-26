import logging
from abc import ABC, abstractmethod
from compiler.code_generator.opcode import Opcode

logger = logging.getLogger(__name__)

class BaseCodeGenerator(ABC):
    """
    Abstract base class for all SQL code generators.
    """
    def __init__(self, ast):
        self.ast = ast
        self.label_counter = 0
        logger.debug("Initialized BaseCodeGenerator with AST: %r", ast)
        
    def new_label(self, prefix="label"):
        self.label_counter += 1
        label = f"{prefix}_{self.label_counter}"
        logger.debug("Generated new label: %s", label)
        return label
        
    @abstractmethod  # This method must be implemented by subclasses
    def generate(self):
        """
        Returns a list of Opcodes that represent the SQL code generated from the AST.
        """
        logger.debug("BaseCodeGenerator.generate() called (should be implemented by subclass)")
        pass