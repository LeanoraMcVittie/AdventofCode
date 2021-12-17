from typing import List

def run(instructions: List[str]) -> str:
	horizontal: int = 0
	depth: int = 0
	aim: int = 0
	for instruction in instructions:
		cmd, val = instruction.split()
		val = int(val)
		if cmd == "down":
			aim += val
		elif cmd == "up":
			aim -= val
		elif cmd == "forward":
			horizontal += val
			depth += aim * val
		else:
			raise Exception("unknown command")
	return str(horizontal * depth)
