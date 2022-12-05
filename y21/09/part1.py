from typing import List

class Field:

	def __init__(self, heights: List[str]) -> None:
		self.vents = [[int(heights[i][j]) for j in range(len(heights[0]))] for i in range(len(heights))]

	def get_vent_value_no_throw(self, x: int, y: int) -> int:
		if x < 0 or y < 0:
			return None
		try:
			return self.vents[x][y]
		except IndexError:
			return None

	def _get_risk_level(self, x: int, y: int) -> int:
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
			return 0
		return vent + 1

def run(input_data: List[str], **kwargs) -> int:
	field = Field(input_data)
	total_risk = 0
	for i in range(len(input_data)):
		for j in range(len(input_data[0])):
			total_risk += field._get_risk_level(i, j)
	return total_risk
