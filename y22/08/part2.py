from typing import List
from utils.field.two_d import Cell, Field

class Tree(Cell):
	scenic_score = 1

	def set_value(self, value) -> None:
		self.value = int(value)

def run(input_data: List[str], **kwargs) -> int:
	field = Field.create_from_input(input_data, Tree)
	for cell in field.gen_cells():
		count = 0
		for y in range(cell.y-1, -1, -1):
			count += 1
			if field.get(cell.x, y).value >= cell.value:
				break
		cell.scenic_score *= count
		
		count = 0
		for y in range(cell.y+1, field.y_size):
			count += 1
			if field.get(cell.x, y).value >= cell.value:
				break
		cell.scenic_score *= count

		count = 0
		for x in range(cell.x-1, -1, -1):
			count += 1
			if field.get(x, cell.y).value >= cell.value:
				break
		cell.scenic_score *= count
		
		count = 0
		for x in range(cell.x+1, field.x_size):
			count += 1
			if field.get(x, cell.y).value >= cell.value:
				break
		cell.scenic_score *= count

	return max(field.gen_cells(transform=lambda c: c.scenic_score))
