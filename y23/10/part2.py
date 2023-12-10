from typing import List, Tuple
from utils.field.two_d import Cell, Coord, Field

SEGMENTS = "|-LJ7F"
CONNECTORS = SEGMENTS + "S"


class LoopCell(Cell):
	distance: int

	def __init__(self, x: int, y: int) -> None:
		super().__init__(x, y)
		self.distance = None

	@property
	def up(self) -> Coord:
		return Coord(self.x - 1, self.y)
	
	@property
	def down(self) -> Coord:
		return Coord(self.x + 1, self.y)

	@property
	def left(self) -> Coord:
		return Coord(self.x, self.y - 1)
	
	@property
	def right(self) -> Coord:
		return Coord(self.x, self.y + 1)
	
	@property
	def up_right(self) -> Coord:
		return Coord(self.x - 1, self.y + 1)
	
	@property
	def up_left(self) -> Coord:
		return Coord(self.x - 1, self.y - 1)
	
	@property
	def down_right(self) -> Coord:
		return Coord(self.x + 1, self.y + 1)
	
	@property
	def down_left(self) -> Coord:
		return Coord(self.x + 1, self.y - 1)
	
	def resolve_s_value(self, is_test) -> str:
		if self.value != "S": 
			return self.value
		return "F" if is_test else "|"

	def get_connectors(self, is_test) -> Tuple[Coord, Coord]:
		return {
			"|": (self.up, self.down),
			"-": (self.left, self.right),
			"L": (self.up, self.right),
			"J": (self.up, self.left),
			"7": (self.left, self.down),
			"F": (self.right, self.down),
		}[self.resolve_s_value(is_test)]

	def get_next(self, prev: Coord, is_test: bool) -> Coord:
		links = self.get_connectors(is_test)
		if links[0] == Coord(prev.x, prev.y):
			return links[1]
		return links[0]

	def set_distance(self, dist: int) -> None:
		self.distance = dist

	def reset_value(self, val: str) -> None:
		self.value = val

class TigerField(Field):
	is_test: bool

	def reduce_to_loop(self) -> None:
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
	
	def apply_distances(self) -> None:
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
	
	def cleanup(self) -> None:
		for c in self.gen_cells(filterer=lambda c: c.value != "." and c.distance is None):
			c.value = "."

	def get_from_coord(self, c: Coord):
		return self.get(c.x, c.y)

	def traverse(self) -> None:
		start = self.first(filterer=lambda a: a.value in SEGMENTS)
		void = start.up
		curr = start
		next = self.get_from_coord(start.get_connectors(self.is_test)[0])

		def set_void(v):
			void_cell = self.get(v.x, v.y)
			if void_cell is not None and void_cell.value == ".":
				void_cell.value = " "

		set_void(void)
			
		while next != start:
			# move void
			seg = next.resolve_s_value(self.is_test)
			if seg == "|":
				if void in [next.up_left, next.down_left]:
					void = next.left
				elif void in [next.up_right, next.down_right]:
					void = next.right
				else: raise Exception("void not in valid location")
			elif seg == "-":
				if void in [next.up_left, next.up_right]:
					void = next.up
				elif void in [next.down_left, next.down_right]:
					void = next.down
				else: raise Exception("void not in valid location")
			elif seg == "F":
				if void == next.down_right:
					void = Coord(curr.x, curr.y)
				elif void == next.up_right:
					set_void(next.up)
					void = next.left
				elif void == next.down_left:
					set_void(next.left)
					void = next.up
				else: raise Exception("void not in valid location")
			elif seg == "J":
				if void == next.up_left:
					void = Coord(curr.x, curr.y)
				elif void == next.up_right:
					set_void(next.right)
					void = next.down
				elif void == next.down_left:
					set_void(next.down)
					void = next.right
				else: raise Exception("void not in valid location")
			elif seg == "L":
				if void == next.up_right:
					void = Coord(curr.x, curr.y)
				elif void == next.down_right:
					set_void(next.down)
					void = next.left
				elif void == next.up_left:
					set_void(next.left)
					void = next.down
				else: raise Exception("void not in valid location")
			elif seg == "7":
				if void == next.down_left:
					void = Coord(curr.x, curr.y)
				elif void == next.down_right:
					set_void(next.right)
					void = next.up
				elif void == next.up_left:
					set_void(next.up)
					void = next.right
				else: raise Exception("void not in valid location")
		
			set_void(void)

			# next in loop
			prev = curr
			curr = next
			next = self.get_from_coord(curr.get_next(prev, self.is_test))

	
	def flood(self) -> None:
		current_cells = list(self.gen_cells(filterer=lambda a: a.value == " "))
		while len(current_cells) > 0:
			[c.reset_value(" ") for c in current_cells]
			next_cells = []
			for c in current_cells:
				next_cells.extend(self.gen_adjacent_cells(c, include_diagonals=False, filterer=lambda a: a.value == "."))
			current_cells = list(set(next_cells))

def run(input_data: List[str], **kwargs) -> int:
	field = TigerField.create_from_input(input_data, LoopCell)
	field.is_test = kwargs["is_test"]
	field.reduce_to_loop()
	field.apply_distances()
	field.cleanup()
	field.traverse()
	field.flood()
	return field.apply(filterer=lambda x: x.value == ".")

