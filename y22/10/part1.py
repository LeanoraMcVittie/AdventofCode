from typing import List

class CPU:
	def __init__(self) -> None:
		self.cycle = 0
		self.sum = 0

	def increment_cycle(self, x):
		self.cycle += 1
		if self.cycle in [20, 60, 100, 140, 180, 220]:
			self.sum += x * self.cycle

def run(input_data: List[str], **kwargs) -> int:
	x = 1
	cpu = CPU()

	for d in input_data:
		instr = d[:4]
		cpu.increment_cycle(x)
		if instr == "noop":
			continue
		else:
			cpu.increment_cycle(x)
			_, val = d.split()
			x += int(val)
	
	return cpu.sum