from typing import List, Tuple
from utils.field.two_d import Cell, Coord, Field

SEGMENTS = "|-LJ7F"
CONNECTORS = SEGMENTS + "S"


class LoopCell(Cell):
	distance: int

	def __init__(self, x: int, y: int) -> None:
		super().__init__(x, y)
		self.distance = None

	def get_connectors(self, is_test) -> Tuple[Coord, Coord]:
		up = Coord(self.x - 1, self.y)
		down = Coord(self.x + 1, self.y)
		left = Coord(self.x, self.y - 1)
		right = Coord(self.x, self.y + 1)
		if self.value == "S":
			if is_test:
				return (down, right)
			return (up, down)
		return {
			"|": (up, down),
			"-": (left, right),
			"L": (up, right),
			"J": (up, left),
			"7": (left, down),
			"F": (right, down),
		}[self.value]
	
	def set_distance(self, dist: int) -> None:
		self.distance = dist


class TigerField(Field):
	is_test: bool

	def reduce_to_loop(self):
		disconnected = True
		while disconnected:
			disconnected = False
			for seg in self.gen_cells(filterer=lambda c: c.value in SEGMENTS):
				neighbors = [self.get(n.x, n.y) for n in seg.get_connectors(self.is_test)]
				if not all(n and n.value in CONNECTORS for n in neighbors):
					seg.value = "."
					disconnected = True
				elif not all(Coord(seg.x, seg.y) in n.get_connectors(self.is_test) for n in neighbors):
					seg.value = "."
					disconnected = True
	
	def apply_distances(self):
		count = 0
		current_cells = [self.first(filterer=lambda c: c.value == "S")]
		while len(current_cells) > 0:
			[c.set_distance(count) for c in current_cells]	
			next_cells = []
			for c in current_cells:
				neighbors = [self.get(n.x, n.y) for n in c.get_connectors(self.is_test)]
				next_cells.extend(n for n in neighbors if n.distance is None)
			current_cells = next_cells
			count += 1

def run(input_data: List[str], **kwargs) -> int:
	field = TigerField.create_from_input(input_data, LoopCell)
	field.is_test = kwargs["is_test"]
	field.reduce_to_loop()
	field.apply_distances()
	return max(field.gen_cells(filterer=lambda c: c.distance is not None, transform=lambda c: c.distance))

