from typing import Dict, Generator, List, Tuple
from utils.field.two_d import Cell, Field 
from utils.math import product
import itertools as it

class Edge():
	def __init__(self, values: Generator[bool, None, None], field_num: int) -> None:
		self.field_num = field_num
		self.edge_values = [v.value for v in values]
		self.match = None

	def matches(self, edge: "Edge") -> Tuple[bool, bool]:
		match = False
		flipped = False
		if self.edge_values == edge.edge_values:
			if self.match and self.match != edge.field_num:
				raise Exception("multiple matches found")
			match = True
			self.match = edge.field_num
			edge.match = self.field_num
		elif self.edge_values == edge.edge_values[::-1]:
			if self.match and self.match != edge.field_num:
				raise Exception("multiple matches found")
			match = True
			self.match = edge.field_num
			edge.match = self.field_num
			flipped = True
		return match, flipped


class Element(Cell):
	def __init__(self, x, y) -> None:
		super(Element, self).__init__(x, y)

	def set_value(self, value: str) -> None:
		self.value = value == "#"


class SegmentField(Field):
	def __init__(self, lines, field_num) -> None:
		super(SegmentField, self).__init__(10, 10, Element)
		self.apply(transform=lambda x: x.set_value(lines[x.x][x.y]))
		self.num = field_num
		self.edges = [
			Edge(self.gen_cells(filterer=lambda x: x.x == 0), self.num),
			Edge(self.gen_cells(filterer=lambda x: x.y == 0), self.num),
			Edge(self.gen_cells(filterer=lambda x: x.x == 9), self.num),
			Edge(self.gen_cells(filterer=lambda x: x.y == 9), self.num),
		]
		self.rotated = 0
		self.flipped = False

	def count_matched_edges(self) -> int:
		return len([edge for edge in self.edges if edge.match])

	def is_match(self, segment: "SegmentField") -> bool:
		return any([e1.matches(e2)[0] for e1, e2 in it.product(self.edges, segment.edges)])
 

class Segment(Cell):
	def __init__(self, x, y, field) -> None:
		super(Segment, self).__init__(x, y)
		self.field = field	


class Puzzle(Field):
	def __init__(self, data) -> None:
		i = 0
		segment_lines = []
		self.segments: Dict[int, SegmentField] = {}
		field_num = None
		for datum in data:
			if datum == "":
				self.segments[field_num] = SegmentField(segment_lines, field_num)
				segment_lines = []
			elif datum.startswith("Tile "):
				field_num = int(datum[5:-1])
			else: segment_lines.append(datum)
		self.segments[field_num] = SegmentField(segment_lines, field_num)
		

	def get_corners(self) -> List[int]:
		for seg1, seg2 in it.combinations(self.segments.values(), 2): seg1.is_match(seg2)

		corners = []
		for seg in self.segments.values():
			if seg.count_matched_edges() <= 2: corners.append(seg.num)
		if len(corners) != 4:
			raise Exception(f"{len(corners)} corners found. whoops")

		return corners




def run(input_data: List[str], **kwargs) -> int:
	puzzle = Puzzle(input_data)
	return product(puzzle.get_corners())