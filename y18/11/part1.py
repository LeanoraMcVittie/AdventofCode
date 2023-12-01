from typing import List
from utils.field.two_d import Cell, Coord, Field

class FuelCell(Cell):
	def power_level(self, serial_number: int) -> int:
		rackID = self.x + 1 + 10
		pl = rackID * (self.y + 1)
		pl += serial_number
		pl *= rackID
		hundreds = int(pl/100) % 10
		return hundreds - 5


def run(input_data: List[str], **kwargs) -> int:
	serial_number = int(input_data[0])
	field = Field(300, 300, FuelCell)
	field.apply(transform=lambda c: c.set_value(c.power_level(serial_number)))
	max_power = 0
	max_cell = None
	for cell in field.gen_cells():
		power = sum(
			field.gen_adjacent_cells(
				cell, transform=lambda c: c.value
			)
		)
		power += cell.value
		if power > max_power:
			max_power = power
			max_cell = cell
	return f"{max_cell.x},{max_cell.y}"
