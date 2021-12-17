from typing import List
import itertools as it
from y19.intcode import IntCode

def run(input_data: List[str]) -> int:
	memory = input_data[0]
	max_thruster_signal = 0
	for phase_settings in it.permutations(range(5)):
		output = 0
		for phase in phase_settings:
			amplifier = IntCode(memory)
			amplifier.add_input(phase)
			amplifier.add_input(output)
			amplifier.run()
			output = amplifier.next_output()
		if output > max_thruster_signal: max_thruster_signal = output
	return max_thruster_signal
