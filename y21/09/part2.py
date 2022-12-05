from typing import List

class Field:

	def __init__(self, heights: List[str]) -> None:
		self.vents = [[int(heights[i][j]) for j in range(len(heights[0]))] for i in range(len(heights))]
		self.visited = [[False for j in range(len(self.vents[0]))] for i in range(len(self.vents))]

	def get_vent_value_no_throw(self, x: int, y: int) -> int:
		if x < 0 or y < 0:
			return None
		try:
			return self.vents[x][y]
		except IndexError:
			return None

	def is_low_point(self, x: int, y: int) -> bool:
		vent = self.vents[x][y]
		neighbor_vents = []
		if any(
			vent >= neighbor 
			for neighbor in [
				self.get_vent_value_no_throw(x, y-1), 
				self.get_vent_value_no_throw(x, y+1),
				self.get_vent_value_no_throw(x-1, y),
				self.get_vent_value_no_throw(x+1, y),
			]
			if neighbor is not None
		):
			return False 
		return True 

	def get_basin_size(self, x: int, y: int) -> bool:
		basin_size = 1
		vent = self.vents[x][y]
		self.visited[x][y] = True
		for i, j in [(x,y+1),(x,y-1),(x+1,y),(x-1,y)]:
			neighbor = self.get_vent_value_no_throw(i,j)
			if (
				neighbor is not None 
				and neighbor > vent 
				and neighbor != 9
				and not self.visited[i][j]
			):
				basin_size += self.get_basin_size(i, j)
		return basin_size

def run(input_data: List[str], **kwargs) -> int:
	field = Field(input_data)
	largest_basins = [0, 0, 0]
	for i in range(len(input_data)):
		for j in range(len(input_data[0])):
			if field.is_low_point(i, j):
				basin_size = field.get_basin_size(i, j)
				if basin_size > largest_basins[0]:
					largest_basins[0] = basin_size
					largest_basins.sort()
	return largest_basins[0] * largest_basins[1] * largest_basins[2]
