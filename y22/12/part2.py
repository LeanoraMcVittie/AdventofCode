from typing import Callable, List, Optional, Tuple
from utils.field.two_d import Cell, Field
from heapq import heappush, heappop


class Rock(Cell):
	elevation: int

	def cost(self, current_value) -> int:
		return 1 if (self.elevation - current_value) <= 1 else 1000000000

	def set_value(self, value) -> None:
		super().set_value(value)
		if self.value == "S":
			self.value = "a"
		if self.value.islower():
			self.elevation = ord(self.value)
		if self.value == "E":
			self.elevation = ord("z")

class Mountain(Field):
	def dijkstra(
		self, 
		start: Cell, 
		end: Cell, 
		include_diagonals: bool = True,
		filterer: Callable[[Cell], bool] = lambda x: True,
	) -> Tuple[Optional[int], Optional[List[Cell]]]:
		unvisited = {i: [] for i in self.gen_cells()}
		it = 0  # sorting hack for heapq
		unvisited[start] = [start]
		reachable = [(0, it, start)]
		while reachable:
			cost_to_current, _, current = heappop(reachable)
			if current not in unvisited:
				continue

			path_to_current = unvisited[current]
			if current is end:
				return cost_to_current, path_to_current

			neighbors = self.gen_adjacent_cells(
				current,
				include_diagonals=include_diagonals,
				filterer=lambda n: n in unvisited and filterer(n),
			)
			for neighbor in neighbors:
				cost = cost_to_current + neighbor.cost(current.elevation)
				path = unvisited[neighbor]
				if path:
					path_cost = 0
					for i in range(len(path)-1):
						path_cost += path[i+1].cost(path[i].elevation)
					if path_cost < cost:
						continue
				path = path_to_current + [neighbor]
				unvisited[neighbor] = path
				it += 1
				heappush(reachable, (cost, it, neighbor))
			del unvisited[current]
		return None, None

def run(input_data: List[str], **kwargs) -> int:
	mtn = Mountain.create_from_input(input_data, Rock)
	start_positions = mtn.gen_cells(filterer=lambda c: c.value == "a")
	min_dist = 500
	for start in start_positions:
		cost, _ = mtn.dijkstra(
			start=start,
			end=mtn.first(filterer=lambda c: c.value == "E"),
			include_diagonals=False,
		)
		if cost < min_dist:
			min_dist = cost
	return min_dist 