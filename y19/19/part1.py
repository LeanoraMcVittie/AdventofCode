from typing import List
from y19.intcode import IntCode

def run(input_data: List[str]) -> int:
	count = 0
	for i in range(0, 50):
		for j in range(0, 50):
			tractor_beam = IntCode(input_data[0])
			tractor_beam.add_input(i)
			tractor_beam.add_input(j)
			tractor_beam.run()
			count += tractor_beam.next_output()
	return count
