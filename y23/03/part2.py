from typing import List, Generator
from utils.field.two_d import Cell, Field 
from math import prod

def run(input_data: List[str], **kwargs) -> int:
	field = Field.create_from_input(input_data, Cell)
	gear_groups = field.gen_cells(
		filterer=lambda a: a.value == "*",
		transform=lambda a: [g for g in field.gen_adjacent_cells(
			cell=a,
			include_diagonals=True,
			filterer=lambda b: b.value in "0123456789"
		)]
	)
	
	total = 0
	for gear_set in gear_groups:
		done = False
		while not done:
			done = True
			for c in gear_set:
				left = field.get(x=c.x, y=c.y+1)
				if left and left.value in "0123456789" and left not in gear_set:
					gear_set.append(left)
					done = False
				right = field.get(x=c.x, y=c.y-1)
				if right and right.value in "0123456789" and right not in gear_set:
					gear_set.append(right)
					done = False
		gear_set.sort()

		gear_nums = []
		while gear_set:
			curr = gear_set.pop(0)
			num = curr.value
			while (
				gear_set
				and curr.x == gear_set[0].x
				and curr.y + 1 == gear_set[0].y
			):
				curr = gear_set.pop(0)
				num += curr.value
			gear_nums.append(int(num))
		
		if len(gear_nums) == 2:
			total += prod(gear_nums)
	
	return total
	