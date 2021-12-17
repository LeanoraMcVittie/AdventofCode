from typing import List
from utils.field.two_d import Cell, Field

class Octopus(Cell):
	def __init__(self, x: int, y: int) -> None:
		super(Octopus, self).__init__(x, y)
		self.flashed = False

	def set_value(self, value: str) -> None:
		self.value = int(value)

	def increment(self) -> None:
		self.value += 1

	def flash(self) -> bool:
		flashed = self.flashed
		self.flashed = True
		return not flashed

	def reset(self) -> None:
		self.value = 0
		self.flashed = False


class OctopodesField(Field):
	def __init__(self, input_field: List[str]) -> None:
		super(OctopodesField, self).__init__(10, 10, Octopus)
		self.apply(transform=lambda x: x.set_value(input_field[x.x][x.y]))

	def cycle(self) -> int:
		self.apply(
			transform=lambda x: x.increment(),
		)

		while self.apply(
			filterer=lambda x: x.value > 9 and x.flash(),
			transform=lambda x: self.apply_adjacent(
				cell=x,
				transform=lambda x: x.increment(),
			),
		): pass

		return self.apply(
			filterer=lambda x: x.flashed,
			transform=lambda x: x.reset(),
		)

	def print(self) -> None:
		for x in range(len(self.items)):
			for y in range(len(self.items[0])):
				print(self.items[x][y].value, end="")
			print()


def run(input_data: List[str]) -> int:
	octopodes = OctopodesField(input_data)
	i = 1
	while octopodes.cycle() < 100: i += 1
	return i 
