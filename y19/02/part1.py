from typing import List
from y19.intcode import IntCode

def run(input_data: List[str]) -> int:
	computer = IntCode(input_data[0])
	computer.codes[1] = 12
	computer.codes[2] = 2
	computer.run()
	return computer.codes[0]
