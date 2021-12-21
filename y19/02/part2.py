from typing import List
from y19.intcode import IntCode
import itertools as it

def run(input_data: List[str]) -> int:
	for i,j in it.product(range(100), range(100)):
		computer = IntCode(input_data[0])
		computer.memory[1] = i
		computer.memory[2] = j
		computer.run()
		if computer.memory[0] == 19690720:
			return i * 100 + j
