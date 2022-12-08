from typing import List
from utils.field.two_d import Cell, Field

class Tree(Cell):
	visible = False

	def set_value(self, value) -> None:
		self.value = int(value)

def run(input_data: List[str], **kwargs) -> int:
	field = Field.create_from_input(input_data, Tree)
	for cell in field.gen_cells():
		if (
			all(field.get(cell.x, y).value < cell.value for y in range(0, cell.y))
			or all(field.get(cell.x, y).value < cell.value for y in range(cell.y + 1, field.y_size))
			or all(field.get(x, cell.y).value < cell.value for x in range(0, cell.x))
			or all(field.get(x, cell.y).value < cell.value for x in range(cell.x + 1, field.x_size))
		):
			cell.visible = True
	return field.apply(filterer=lambda c: c.visible)
