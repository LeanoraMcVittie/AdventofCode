from typing import Dict, List, Optional, Tuple
from y19.intcode import IntCode, WaitingOnInput
from functools import partial
from utils.field.two_d import Cell, Coord, Field
from heapq import heapify, heappush, heappop


FIELDSIZE: int = 44


class Loc(Cell):
	def cost(self) -> int:
		return 1 if self.value != "#" else 10000000

	def __str__(self) -> str:
		return self.value or " "

class DijkstraNode:
	def __init__(self, cell: Cell, cost: Optional[int] = None) -> None:
		self.cost = cost
		self.cell = cell
		self.prev = None

	def __lt__(self, other: "DijkstraNode") -> bool:
		return self.cost < other.cost

	def update_cost(self, new_cost: int, prev: "DijkstraNode") -> bool:
		if self.cost is None or self.cost > new_cost:
			self.cost = new_cost
			self.prev = prev
			return True
		return False

	def get_path(self) -> List[Cell]:
		prev_path = self.prev.get_path() if self.prev is not None else []
		return prev_path + [self.cell]


class OxygenField(Field):
	# TERRIBLE implementation - good enough for this, so can't be bothered to fix
	def dijkstra(self, start: Cell, end: Cell, include_diagonals: bool = False) -> DijkstraNode:
		visited: List[Cell] = []
		to_visit: List[DijkstraNode] = [DijkstraNode(start, cost=0)]
		coord_to_dijkstranode: Dict[Tuple[int, int], DijkstraNode] = {(start.x, start.y): to_visit[0]}
		while True:
			assert to_visit
			visit = heappop(to_visit)
			visited.append(visit.cell)
			if visit.cell is end: return visit
			resort = False
			for n in self.gen_adjacent_cells(
				visit.cell,
				include_diagonals=include_diagonals,
				filterer=lambda n: n not in visited,
			):
				dn = coord_to_dijkstranode.setdefault((n.x, n.y), DijkstraNode(n))
				if dn.update_cost(visit.cost + n.cost(), visit) and dn in to_visit: resort = True
				elif dn not in to_visit: heappush(to_visit, dn)
			if resort: heapify(to_visit)


class Droid(Coord):
	def __init__(self, memory: str) -> None:
		super(Droid, self).__init__(int(FIELDSIZE / 2), int(FIELDSIZE / 2))
		self.computer = IntCode(memory)

	def horizontal(self, amt: int) -> None:
		self.y += amt
		if self.y not in range(FIELDSIZE): raise Exception("Need a bigger field!")

	def vertical(self, amt: int) -> None:
		self.x += amt
		if self.x not in range(FIELDSIZE): raise Exception("Need a bigger field!")

	def move(self, direction: str) -> int:
		self.computer.add_input(
			{
				"n": 1,
				"s": 2,
				"w": 3,
				"e": 4,
			}[direction]
		)
		try: self.computer.run()
		except WaitingOnInput: pass
		status = self.computer.next_output()
		if status != 0:
			{
				"n": partial(self.vertical, -1),
				"s": partial(self.vertical, 1),
				"e": partial(self.horizontal, 1),
				"w": partial(self.horizontal, -1),
			}[direction]()
		return status

	def determine_direction(self, loc: Loc) -> str:
		if not loc.is_neighbor(self, False):
			raise Exception("determinig direction to a non-neighbor")
		x_diff = self.x - loc.x
		y_diff = self.y - loc.y
		return {
			(1, 0): "n",
			(-1, 0): "s",
			(0, -1): "e",
			(0, 1): "w",
		}[(x_diff, y_diff)]

	def follow_path(self, path: List[Loc]) -> None:
		for elem in path:
			try:
				self.move(self.determine_direction(elem))
			except Exception as e:
				import pdb; pdb.set_trace()


class Oxygen:
	def __init__(self, droid: Droid) -> None:
		self.droid = droid
		self.field = OxygenField(FIELDSIZE, FIELDSIZE, Loc)
		self.oxygen_cell: Loc = None
		self.start_cell: Loc = self.field.get(self.droid.x, self.droid.y)
		self.start_cell.set_value(".")

	def map(self) -> None:
		to_test: List[Loc] = [self.start_cell]
		next_to_test = None
		while to_test or next_to_test:
			testing = next_to_test
			next_to_test = None
			if not testing:
				testing = to_test.pop()
				droid_path = self.field.dijkstra(
					self.field.get(self.droid.x, self.droid.y),
					testing,
				).get_path()[1:]
			else:
				droid_path = [testing]
			self.droid.follow_path(droid_path)

			for direction, x_offset, y_offset in [("n", -1, 0), ("s", 1, 0), ("e", 0, 1), ("w", 0, -1)]:
				neighbor = self.field.get(self.droid.x + x_offset, self.droid.y + y_offset)
				if neighbor.value: continue
				status = self.droid.move(direction)
				if status == 0:
					neighbor.set_value("#")
				else:
					neighbor.set_value(".")
					self.droid.move({"n": "s", "s": "n", "e": "w", "w": "e"}[direction])
					if not next_to_test: next_to_test = neighbor
					else: to_test.append(neighbor)
					if status == 2:
						assert not self.oxygen_cell or self.oxygen_cell is neighbor
						self.oxygen_cell = neighbor

	def distance_to_oxygen_system(self) -> int:
		return self.field.dijkstra(self.start_cell, self.oxygen_cell).cost


def run(input_data: List[str]) -> int:
	droid = Droid(input_data[0])
	oxygen = Oxygen(droid)
	oxygen.map()
	oxygen.field.print()
	return oxygen.distance_to_oxygen_system()
