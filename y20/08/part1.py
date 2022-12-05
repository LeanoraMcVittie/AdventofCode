from typing import List


def run(input_data: List[str], **kwargs) -> int:
	i: int = 0
	accumulator: int = 0
	visited_instructions: List[int] = []
	while True:
		visited_instructions.append(i)
		instr, amt = input_data[i].split(" ")
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
			return accumulator

