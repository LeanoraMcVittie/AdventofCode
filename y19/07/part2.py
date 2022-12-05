from typing import List
import itertools as it
from y19.intcode import Halted, IntCode, WaitingOnInput

def run(input_data: List[str], **kwargs) -> int:
	memory = input_data[0]
	max_thruster_signal = 0
	for phase_settings in it.permutations(range(5, 10)):
		output = 0
		amplifiers = []
		for i in range(5):
			amplifier = IntCode(memory)
			amplifier.add_input(phase_settings[i])
			amplifiers.append(amplifier)

		try:
			i = 0
			while True:
				amplifier = amplifiers[i]
				amplifier.add_input(output)
				try:
					amplifier.run()
				except WaitingOnInput:
					pass
				output = amplifier.next_output()
				i = (i + 1) % 5
		except Halted:
			pass

		final_output = amplifiers[4].last_output()
		if final_output > max_thruster_signal:
			max_thruster_signal = final_output

	return max_thruster_signal
