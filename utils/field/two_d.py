from typing import Any, Callable, Generator, List, Optional, Union


class Cell:
	def __init__(self, x: int, y: int) -> None:
		self.value = None
		self.x = x
		self.y = y

	def set_value(self, value: Any) -> Any:
		self.value = value

class Field:
	items: List[List[Cell]]

	def __init__(self, x_size: int, y_size: int, cell_class: Callable) -> None:
		self.items = [
			[
				cell_class(x, y) for y in range(y_size)
			] 
			for x in range(x_size)
		]

	def get(self, x: int, y: int, default: Any = None) -> Union[Optional[Cell], Any]:
		if x < 0 or y < 0:
			return default
		try:
			return self.items[x][y]
		except IndexError:
			return default

	def gen_adjacent_cells(
		self, 
		cell: Cell,
		include_diagonals: bool = True, 
		transform: Callable = lambda x: x,
		filterer: Callable = lambda x: True,
	) -> Generator[Cell, None, None]:
		for x in range(cell.x-1, cell.x+2):
			for y in range(cell.y-1, cell.y+2):
				neighbor = self.get(x, y)
				if (
					neighbor is not None
					and neighbor != cell
					and (
						include_diagonals
						or neighbor.x == cell.x
						or neighbor.y == cell.y
					)
					and filterer(neighbor)
				):
					yield transform(neighbor)

	def apply_adjacent(
		self, 
		cell: Cell,
		include_diagonals: bool = True, 
		transform: Callable = lambda x: x,
		filterer: Callable = lambda x: True,
	) -> int:
		return len(
			[
				cell for cell in self.gen_adjacent_cells(
					cell, include_diagonals, transform, filterer
				)
			]
		)

	def gen_cells(
		self, 
		transform: Callable = lambda x: x, 
		filterer: Callable = lambda x: True
	) -> Generator[Cell, None, None]:
		for x in range(len(self.items)):
			for y in range(len(self.items[0])):
				if filterer(self.items[x][y]):
					yield transform(self.items[x][y])


	def apply(
		self, 
		transform: Callable = lambda x: x, 
		filterer: Callable = lambda x: True
	) -> None:
		return len([cell for cell in self.gen_cells(transform, filterer)])


	def clone(self, for_rotating: bool = False) -> "Field":
		x_size = len(self.items) if for_rotating else len(self.items[0])
		y_size = len(self.items[0]) if for_rotating else len(self.items)
		new_field = type(self)(y_size, x_size, type(self.items[0][0]))
		return new_field

	def rotate(self) -> "Field":
		# clockwise
		rotated_field = self.clone(for_rotating=True)
		rotated_field.apply(
			transform=lambda x: x.set_value(self.items[x.y][len(self.items)-(x.x+1)].value)
		)
		return rotated_field

	def switch_top_bottom(self) -> "Field":
		flipped_field = self.clone()
		flipped_field.apply(
			transform=lambda x: x.set_value(
				self.items[int(len(self.items[0])/2)-(x.x-int((len(self.items[0])+1)/2))-1][x.y].value
			)
		)
		return flipped_field

	def switch_left_right(self) -> "Field":
		flipped_field = self.clone()
		flipped_field.apply(
			transform=lambda x: x.set_value(
				self.items[x.x][int(len(self.items)/2)-(x.y-int((len(self.items)+1)/2))-1].value
			)
		)
		return flipped_field

	def print(self) -> None:
		for x in range(len(self.items)):
			for y in range(len(self.items[0])):
				print(self.items[x][y].value, end="")
			print()
		print()