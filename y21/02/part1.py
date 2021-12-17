from typing import List

def run(instructions: List[str]) -> str:
	horizontal: int = 0
	depth: int = 0
	for instruction in instructions:
		cmd, val = instruction.split()
		if cmd == "down":
			depth += int(val)
		elif cmd == "up":
			depth -= int(val)
		elif cmd == "forward":
			horizontal += int(val)
		else:
			raise Exception("unknown command")
	return str(horizontal * depth)
