from typing import Dict, Generator, List, Tuple
from utils.field.two_d import Cell, Field 
from utils.math import product
from math import sqrt
import itertools as it


class Edge():
	def __init__(self, values: Generator[bool, None, None], field_num: int) -> None:
		self.field_num = field_num
		self.edge_values = [v.value for v in values]
		self.match = None
		self.flipped = False

	def matches(self, edge: "Edge") -> bool:
		if self.edge_values == edge.edge_values:
			if self.match and self.match != edge:
				raise Exception("multiple matches found")
			self.match = edge
			edge.match = self
		elif self.edge_values == edge.edge_values[::-1]:
			if self.match and self.match != edge:
				raise Exception("multiple matches found")
			self.match = edge
			edge.match = self
			self.flipped = True
		return self.match is not None

	def flip(self) -> None:
		self.flipped = not self.flipped

	def should_reverse_polarity(self) -> bool:
		if not self.match:
			return False
		return self.flipped != self.match.flipped

	def print(self) -> None:
		for v in self.edge_values:
			print("#" if v else ".", end="")
		print()


class Element(Cell):
	def __init__(self, x, y) -> None:
		super(Element, self).__init__(x, y)

	def set_value_from_hash(self, value: str) -> None:
		self.value = value == "#"


class SegmentField(Field):
	def clone(self, for_rotating: bool = False) -> "SegmentField":
		new_field = super(SegmentField, self).clone(for_rotating)
		new_field.num = self.num
		new_field.edges = self.edges
		return new_field

	def rotate(self) -> "SegmentField":
		print("rotate")
		rotated_field = super(SegmentField, self).rotate()
		popped_edge = rotated_field.edges.pop(-1)
		rotated_field.edges.insert(0, popped_edge)
		rotated_field.edges[1].flip()
		rotated_field.edges[3].flip()
		rotated_field.print()
		return rotated_field

	def switch_top_bottom(self) -> "SegmentField":
		print("flip top and bottom")
		flipped_field = super(SegmentField, self).switch_top_bottom()
		tmp = flipped_field.edges[0]
		flipped_field.edges[0] = flipped_field.edges[2]
		flipped_field.edges[2] = tmp
		flipped_field.edges[1].flip()
		flipped_field.edges[3].flip()
		flipped_field.print()
		return flipped_field

	def switch_left_right(self) -> "SegmentField":
		print("flip left and right")
		flipped_field = super(SegmentField, self).switch_left_right()
		tmp = flipped_field.edges[1]
		flipped_field.edges[1] = flipped_field.edges[3]
		flipped_field.edges[3] = tmp
		flipped_field.edges[0].flip()
		flipped_field.edges[2].flip()
		flipped_field.print()
		return flipped_field

	@classmethod
	def create_from_field_lines(cls, lines, field_num) -> "SegmentField":
		field = cls(10, 10, Element)
		field.apply(transform=lambda x: x.set_value_from_hash(lines[x.y][x.x]))
		field.num = field_num
		field.edges = [
			Edge(field.gen_cells(filterer=lambda x: x.x == 0), field.num), # top
			Edge(field.gen_cells(filterer=lambda x: x.y == 0), field.num), # left
			Edge(field.gen_cells(filterer=lambda x: x.x == 9), field.num), # bottom
			Edge(field.gen_cells(filterer=lambda x: x.y == 9), field.num), # right
		]
		return field

	def get_bottom_edge(self) -> Edge:
		return self.edges[2]

	def get_right_edge(self) -> Edge:
		return self.edges[3]

	def get_right_segment(self) -> "SegmentField":
		return self.get_right_edge().match.field_num

	def get_bottom_segment(self) -> "SegmentField":
		return self.get_bottom_edge().match.field_num

	def count_matched_edges(self) -> int:
		return len([edge for edge in self.edges if edge.match])

	def is_match(self, segment: "SegmentField") -> bool:
		return any([e1.matches(e2) for e1, e2 in it.product(self.edges, segment.edges)])

	def orient(self, expected_top: Edge, expected_left: Edge) -> None:
		oriented_seg = self
		if expected_top and expected_top.should_reverse_polarity():
			oriented_seg = oriented_seg.switch_left_right()
		if expected_left and expected_left.should_reverse_polarity():
			oriented_seg = oriented_seg.switch_top_bottom()

		def matched_correctly(expected_edge: Edge, matched_edge) -> bool:
			if not expected_edge:
				return matched_edge is None
			if not matched_edge:
				return False
			if matched_edge.field_num != expected_edge.field_num:
				return False
			if matched_edge.flipped != expected_edge.flipped:
				import pdb; pdb.set_trace()
				return False
			return True

		def line_up_top_and_flip(oriented_seg):
			for _ in range(4):
				if matched_correctly(oriented_seg.edges[0].match, expected_top):
					break
				oriented_seg = oriented_seg.rotate()
			else:
				import pdb; pdb.set_trace()
		
			if not matched_correctly(oriented_seg.edges[1].match, expected_left):
				oriented_seg = oriented_seg.switch_left_right()
			return oriented_seg
		
		oriented_seg = line_up_top_and_flip(oriented_seg)
		if not (
			matched_correctly(oriented_seg.edges[0].match, expected_top)
			and matched_correctly(oriented_seg.edges[1].match, expected_left)
		) and oriented_seg.count_matched_edges() == 2:
			print("corner piece - rotating again")
			oriented_seg = oriented_seg.rotate()
			oriented_seg = line_up_top_and_flip(oriented_seg)
		try:
			assert matched_correctly(oriented_seg.edges[0].match, expected_top)
			assert matched_correctly(oriented_seg.edges[1].match, expected_left)
		except Exception as e:
			import pdb; pdb.set_trace()
			raise e
		return oriented_seg


class Puzzle(Field):
	@classmethod
	def create_from_input_data(cls, data) -> "Puzzle":
		i = 0
		segment_lines = []
		segments: Dict[int, SegmentField] = {}
		field_num = None
		for datum in data:
			if datum == "":
				segments[field_num] = SegmentField.create_from_field_lines(segment_lines, field_num)
				segment_lines = []
			elif datum.startswith("Tile "):
				field_num = int(datum[5:-1])
			else: segment_lines.append(datum)
		segments[field_num] = SegmentField.create_from_field_lines(segment_lines, field_num)
		for seg1, seg2 in it.combinations(segments.values(), 2): seg1.is_match(seg2)
		size = int(sqrt(len(segments)))

		for seg in segments.values():
			if seg.count_matched_edges() <= 2:
				corner = seg
				break
		else:
			raise Exception("no corners found") 
		segment_map = [[None for _ in range(size)] for _ in range(size)]
		segment_map[0][0] = corner
		
		def print_seg_map():
			for y in range(size):
				for x in range(size):
					if segment_map[y][x]:
						print(segment_map[y][x].num, end=" ")
					else: print("    ", end = " ")
				print()
			print()


		for x, y in it.product(range(size), range(size)):
			print(segment_map[x][y].num)
			segment_map[x][y].print()
			expected_top = None if x == 0 else segment_map[x-1][y].get_bottom_edge()
			expected_left = None if y == 0 else segment_map[x][y-1].get_right_edge()
			segment_map[x][y] = segment_map[x][y].orient(expected_top, expected_left)
			if y+1 < size:
				right = segments[segment_map[x][y].get_right_segment()]
				segment_map[x][y+1] = right
			if x+1 < size:
				bottom = segments[segment_map[x][y].get_bottom_segment()]
				segment_map[x+1][y] = bottom
			print_seg_map()

		completed_puzzle = cls(size*8, size*8, Element)
		for x, y in it.product(range(size), range(size)):
			# loop through each segment
			seg = segment_map[x][y]
			for i in range(1, 9):
				for j in range(1, 9):
					# loop through each element of the segment
					puzz_x = x*8 + i - 1
					puzz_y = y*8 + j - 1
					completed_puzzle.items[puzz_x][puzz_y].value = seg.items[i][j].value
		completed_puzzle.print()
		return completed_puzzle

	def count_snakes(self) -> int:
		body_positions = [
			(0,1),
			(1,2),
			(4,2),
			(5,1),
			(6,1),
			(7,2),
			(10,2),
			(11,1),
			(12,1),
			(13,2),
			(16,2),
			(17,1),
			(18,0),
			(18,1),
			(19,1),
		]
		snakes = 0
		for x in range(0, len(self.items)-20):
			for y in range(0, len(self.items[0])-2):
				if all(self.items[x+i][y+j].value for i,j in body_positions):
					snakes += 1
		return snakes

def run(input_data: List[str]) -> int:
	puzzle = Puzzle.create_from_input_data(input_data)
	transforms = [
		"rotate", 
		"rotate", 
		"rotate", 
		"switch_left_right", 
		"rotate", 
		"rotate", 
		"rotate", 
		"switch_top_bottom",
		"rotate", 
		"rotate", 
		"rotate", 
		"switch_left_right", 
		"rotate", 
		"rotate", 
		"rotate", 
	]
	for trans in transforms:
		snakes = puzzle.count_snakes()
		if snakes > 0:
			break
		print(trans)
		puzzle = getattr(puzzle, trans)()
	else:
		raise Exception("no snakes found")

	puzzle.print()
	snake_body_count = snakes * 15
	total_pieces = puzzle.apply(filterer=lambda x: x.value)
	return total_pieces - snake_body_count
