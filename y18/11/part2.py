from typing import List
from utils.field.two_d import Cell, Coord, Field


GRID_SIZE: int = 300


class FuelCell(Cell):
	def power_level(self, serial_number: int) -> int:
		rackID = self.x + 1 + 10
		pl = rackID * (self.y + 1)
		pl += serial_number
		pl *= rackID
		hundreds = int(pl/100) % 10
		self.power = hundreds - 5
		self.value = f"  {self.power}" if self.power >= 0 else f" {self.power}" 
		self.powers = [self.power]
		return self.power

	def append(self, *args):
		self.powers.append(self.powers[-1] + sum(args))

	def get_max(self) -> int:
		return max(self.powers)
	
	def format_max(self, max_val) -> str:
		idx = self.powers.index(max_val)
		return f"{self.x + 1},{self.y + 1},{idx + 1}"


def run(input_data: List[str], **kwargs) -> int:
	serial_number = int(input_data[0])
	field = Field(GRID_SIZE, GRID_SIZE, FuelCell)
	field.apply(transform=lambda c: c.power_level(serial_number))
	orig_x_sums = [p for p in field.gen_cells_in_range(0, 0, 0, GRID_SIZE - 1, transform=lambda c: c.power)]
	for i in range(1, GRID_SIZE):
		for idx in range(i, len(orig_x_sums)):
			orig_x_sums[idx] += field.get(i, idx).power
		for x in range(0, GRID_SIZE - i):
			if x == 0:
				x_sums = orig_x_sums.copy()
			else:
				for idx in range(i, len(x_sums)):
					x_sums[idx] -= field.get(x - 1, idx).power
					x_sums[idx] += field.get(x + i, idx).power
			for y in range(0, GRID_SIZE - i):
				if y == 0:
					y_sum = sum(field.gen_cells_in_range(
						x + i,
						x + i,
						0,
						i,
						transform=lambda c: c.power
					))
				else:
					y_sum -= field.get(x + i, y - 1).power
					y_sum += field.get(x + i, y + i).power
				field.get(x, y).append(
					x_sums[y + i],
					y_sum,
					-field.get(x + i, y + i).power
				)

	max_power = 0
	max_cell = None
	for cell in field.gen_cells():
		if (cell_max := cell.get_max()) > max_power:
			max_power = cell_max
			max_cell = cell
	return max_cell.format_max(max_power)