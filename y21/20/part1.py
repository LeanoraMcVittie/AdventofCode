from typing import Callable, Generator, List
from utils.field.two_d import Cell, Field


class Image(Field):
	@classmethod
	def create_from_input(cls, input_lines: List[str]) -> "Image":
		field = cls(len(input_lines)+2, len(input_lines[0])+2, Cell)
		field.apply(
			filterer=lambda x: x.x in range(1, len(input_lines)+1) and x.y in range(1, len(input_lines[0])+1),
			transform=lambda x: x.set_value(input_lines[x.x-1][x.y-1])
		)
		return field

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
					(
						include_diagonals
						or neighbor.x == cell.x
						or neighbor.y == cell.y
					)
					and filterer(neighbor)
				):
					yield transform(neighbor)

	def enhance(self, algorithm: str, default_true: bool) -> "Image":
		def set_pixel(pixel: Cell) -> None:
			old_pixel = self.items[pixel.x-1][pixel.y-1]

			def binary_value(neighbor):
				if neighbor is None:
					return "1" if default_true else "0"
				return "1" if neighbor.value == "#" else "0"

			binary_cells = [
				c for c in self.gen_adjacent_cells(
					old_pixel,
					include_diagonals=True,
					transform=binary_value,
				)
			]
			loc = int(str.join("", binary_cells), base=2)
			pixel.value = algorithm[loc]

		new_image = Image(len(self.items)+2, len(self.items[0])+2, Cell)
		new_image.apply(transform=lambda x: x.set_value("#" if not default_true else "."))
		new_image.apply(
			filterer=lambda x: x.x in range(1, len(self.items)+1) and x.y in range(1, len(self.items[0])+1),
			transform=set_pixel,
		)
		return new_image

	def print(self) -> None:
		for x in range(len(self.items)):
			for y in range(len(self.items[0])):
				p = "█" if self.items[x][y].value == "#" else " "
				print(p, end="")
			print()
		print()


def run(input_data: List[str], **kwargs) -> int:
	algorithm = input_data[0]
	image = Image.create_from_input(input_data[2:])
	for i in range(2):
		image = image.enhance(algorithm, default_true=i%2!=0)
	return image.apply(filterer=lambda x: x.value == "#")
