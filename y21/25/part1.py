from typing import List, Tuple
from utils.field.two_d import Cell, Field
from functools import partial


class CucumberSpot(Cell):
	def __bool__(self) -> bool:
		return (
			self.value is not None and self.value != "."
		)

	def get_next_cell_coords(self, xlen: int, ylen: int) -> Tuple[int, int]:
		if self.value == "v":
			return (self.x + 1) % xlen, self.y
		elif self.value == ">":
			return self.x, (self.y + 1) % ylen
		else: raise Exception("Not a cucumber cell")


class SeaCucumbers(Field):
	def move(self, direction: str) -> "SeaCucumbers":
		moved = self.clone()
		for c in self.gen_cells(filterer=lambda c: c):
			move_to_cell_coords = c.get_next_cell_coords(len(self.items), len(self.items[0]))
			if c.value == direction and not self.get(*move_to_cell_coords):
				moved.get(*move_to_cell_coords).set_value(c.value)
			else:
				moved.get(c.x, c.y).set_value(c.value)
		return moved


def run(input_data: List[str], **kwargs) -> int:
	sea_cucumbers_next = SeaCucumbers.create_from_input(input_data, CucumberSpot)
	sea_cucumbers_prev = None
	i: int = 0
	while sea_cucumbers_prev != sea_cucumbers_next:
		i += 1
		sea_cucumbers_prev = sea_cucumbers_next
		sea_cucumbers_next = sea_cucumbers_prev.move(">").move("v")
		# this actually looks really cool
		sea_cucumbers_next.print()
	return i
