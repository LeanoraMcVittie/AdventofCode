from typing import List

def run_program(instructions: List[str]) -> int:
	i: int = 0
	accumulator: int = 0
	visited_instructions: List[int] = []
	while True:
		visited_instructions.append(i)
		instr, amt = instructions[i].split(" ")
		amt = int(amt)
		if instr == "nop":
			i += 1
		elif instr == "acc":
			accumulator += amt 
			i += 1
		elif instr == "jmp":
			i += amt
		else:
			raise Exception("ohno")

		if i in visited_instructions:
			return 0
		if i >= len(instructions):
			return accumulator

def run(instructions: List[str]) -> int:
	for i in range(0, len(instructions)):
		instr, amt = instructions[i].split(" ")
		if instr == "nop":
			instructions[i] = f"jmp {amt}"
			result = run_program(instructions)
			if result != 0:
				return result
			instructions[i] = f"nop {amt}"
		elif instr == "jmp":
			instructions[i] = f"nop {amt}"
			result = run_program(instructions)
			if result != 0:
				return result
			instructions[i] = f"jmp {amt}"
		elif instr == "acc": 
			pass
		else:
			raise Exception("strange")

