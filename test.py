from core.virtual_machine import VirtualMachine, Opcode

class VirtualMachineTest(VirtualMachine):
    def op_load_const(self, value):
        print(f"Loaded: {value}")
        self.registers.append(value)

plan = [
    (Opcode.LOAD_CONST, 42),
    (Opcode.LOAD_CONST, 7)
]
vm = VirtualMachineTest(plan)
vm.run()

