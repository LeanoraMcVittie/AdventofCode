from typing import List
from utils.field.three_d import Cell, Field


class Cube(Cell):
	def __init__(self, x: int, y: int, z: int) -> None:
		super(Cube, self).__init__(x, y, z)
		self.value = False


class GameField(Field):
	def __init__(self, x_size: int, y_size: int, z_size: int) -> None:
		self.x_size = x_size
		self.y_size = y_size
		self.z_size = y_size
		super(GameField, self).__init__(x_size, y_size, z_size, Cube)

	@classmethod
	def create_from_input(cls, input_data: List[str]) -> "GameField":
		x_size = len(input_data)
		y_size = len(input_data[0])
		gamefield = cls(x_size+12, y_size+12, 12)

		def add_value(cube: Cube) -> None:
			cube.value = input_data[cube.x-6][cube.y-6] == "#"

		gamefield.apply(
			filterer = lambda x: (
				x.x in range(6, 6+x_size) 
				and x.y in range(6, 6+y_size) 
				and x.z == 6
			),
			transform = add_value,
		)

		return gamefield

	@classmethod
	def cycle(cls, old: "GameField") -> "GameField":
		new = cls(old.x_size, old.y_size, old.z_size)

		def update_value(new_cube: Cube) -> None:
			old_cube = old.get(new_cube.x, new_cube.y, new_cube.z)
			if not old_cube:
				new_cube.value = False
				return
			n_count = sum(
				1 for n in old.gen_adjacent_cells(
					cell=old_cube,
					filterer=lambda x: x.value,
				)
			)
			if n_count < 2 or n_count > 3:
				new_cube.value = False
			elif old_cube.value:
				new_cube.value = True
			else:
				new_cube.value = n_count == 3

		new.apply(transform=update_value)
		return new

	def print_layer(self, z: int) -> None:
		for x in range(len(self.items)):
			for y in range(len(self.items[0])):
				print("#", end="") if self.get(x, y, z).value else print(".", end="")
			print()

	def count(self) -> int:
		return sum(1 for cube in self.gen_cells(filterer = lambda x: x.value))


def run(input_data: List[str], **kwargs) -> int:
	gamefield = GameField.create_from_input(input_data)
	for _ in range(6):
		gamefield = GameField.cycle(gamefield)
	return gamefield.count()
