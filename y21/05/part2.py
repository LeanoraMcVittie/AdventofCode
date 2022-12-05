from typing import Generator, List, Tuple

FIELD_SIZE: int = 1000

class Line:
	x1: int
	y1: int
	x2: int
	y2: int

	def __init__(self, line: str) -> None:
		start, end = line.split(" -> ")
		x1, y1 = start.split(",")
		x2, y2 = end.split(",")
		self.x1 = int(x1)
		self.x2 = int(x2)
		self.y1 = int(y1)
		self.y2 = int(y2)

	def is_flat(self) -> bool:
		return self.x1 == self.x2 or self.y1 == self.y2

	def gen_coordinates(self) -> Generator[Tuple[int, int], None, None]:
		for i in range(0, (abs(self.x1-self.x2) or abs(self.y1-self.y2)) + 1):
			x = self.x1 + (i * (0 if self.x1 == self.x2 else 1 if self.x1 < self.x2 else -1))
			y = self.y1 + (i * (0 if self.y1 == self.y2 else 1 if self.y1 < self.y2 else -1))
			yield x, y


class Field:
	field: List[List[int]]
	overlaps: int

	def __init__(self) -> None:
		self.field = [[0 for x in range(0, FIELD_SIZE)] for y in range(0, FIELD_SIZE)]
		self.overlaps = 0

	def print(self) -> None:
		for row in self.field:
			print(str.join("", [str(elem) for elem in row]))

	def mark_line(self, line: Line) -> None:
		for x, y in line.gen_coordinates():
			self.field[y][x] += 1
			if self.field[y][x] == 2:
				self.overlaps += 1


def run(input_data: List[str], **kwargs) -> int:
	lines: List[Line] = [Line(datum) for datum in input_data]
	field = Field()
	for line in lines:
		field.mark_line(line)
	return field.overlaps

