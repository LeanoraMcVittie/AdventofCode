from typing import List, Generator
from utils.field.two_d import Cell, Field 


def run(input_data: List[str], **kwargs) -> int:
	field = Field.create_from_input(input_data, Cell)
	adjacent_nums_gen = [g for g in field.gen_cells(
		filterer=lambda a: a.value not in "0123456789.",
		transform=lambda a: field.gen_adjacent_cells(
			cell=a,
			include_diagonals=True,
			filterer=lambda b: b.value in "0123456789"
		)
	)]
	adjacent_nums = []
	for cell_list in adjacent_nums_gen:
		if not isinstance(cell_list, Generator): continue
		adjacent_nums.extend([a for a in cell_list])
	
	done = False
	while not done:
		done = True
		for c in adjacent_nums:
			left = field.get(x=c.x, y=c.y+1)
			if left and left.value in "0123456789" and left not in adjacent_nums:
				adjacent_nums.append(left)
				done = False
			right = field.get(x=c.x, y=c.y-1)
			if right and right.value in "0123456789" and right not in adjacent_nums:
				adjacent_nums.append(right)
				done = False
	
	adjacent_nums.sort()
	total = 0
	while adjacent_nums:
		curr = adjacent_nums.pop(0)
		num = curr.value
		while (
			adjacent_nums
			and curr.x == adjacent_nums[0].x
			and curr.y + 1 == adjacent_nums[0].y
		):
			curr = adjacent_nums.pop(0)
			num += curr.value
		total += int(num)
	return total
	