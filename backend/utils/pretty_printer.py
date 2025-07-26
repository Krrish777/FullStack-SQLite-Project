def pretty_print_plan(plan):
    print("Execution Plan:")
    for index, instr in enumerate(plan):
        opcode = instr[0].name if hasattr(instr[0], 'name') else instr[0]
        operands = ', '.join(str(op) for op in instr[1:]) if len(instr) > 1 else ''
        print(f"  {index:02d}: {opcode} {operands}")