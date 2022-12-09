from typing import List
from utils.field.two_d import Cell, Field

class Loc(Cell):
	def __init__(self, x: int, y: int) -> None:
		super().__init__(x, y)
		self.visited = False 


def run(input_data: List[str], is_test) -> int:
	if is_test:
		field_size = 20 
	else:
		field_size = 1000
	field = Field(field_size, field_size, Loc)
	rope = [field.get(field_size//2, field_size//2)] * 10
	for d in input_data:
		direction, distance = d.split()
		for _ in range(int(distance)):
			head = rope[0]
			head = field.get(*{
				"R": (head.x + 1, head.y),
				"L": (head.x - 1, head.y),
				"U": (head.x, head.y - 1),
				"D": (head.x, head.y + 1),
			}[direction])
			head.value = 0
			rope[0] = head
			for i in range(1, 10):
				head = rope[i-1]
				tail = rope[i]
				if not head.is_neighbor(tail) and head is not tail:
					if head.x == tail.x:
						sign = 1 if head.y > tail.y else -1
						tail = field.get(tail.x, tail.y + (1 * sign))
					elif head.y == tail.y:
						sign = 1 if head.x > tail.x else -1
						tail = field.get(tail.x + (1 * sign), tail.y)
					else:
						y_sign = 1 if head.y > tail.y else -1
						x_sign = 1 if head.x > tail.x else -1
						tail = field.get(tail.x + (1 * x_sign), tail.y + (1 * y_sign))
					rope[i] = tail
			rope[9].visited = True
	return field.apply(filterer=lambda c: c.visited)
