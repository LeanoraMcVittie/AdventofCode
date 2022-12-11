from typing import List

class CPU:
	def __init__(self) -> None:
		self.position = 0

	def increment_cycle(self, x):
		self.position += 1
		if self.position == 41:
			print()
			self.position = 1

		if self.position in [x, x+1, x+2]:
			print("❄️ ", end="")
		else:
			print("🎄", end="")


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
	print()
	return 0