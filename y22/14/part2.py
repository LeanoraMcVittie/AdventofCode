from typing import List
from utils.field.two_d import Cell, Field
from utils.utils import int_split

def get_sign(a, b):
	if a == b: return 1
	return (a-b)//abs(a-b)

def run(input_data: List[str], is_test, **kwargs) -> int:
	if is_test: field = Field(20, 200, Cell)
	else: field = Field(200, 1000, Cell)
	for d in input_data:
		coords_list = d.split(" -> ")
		for i in range(len(coords_list) - 1):
			start_coords = int_split(coords_list[i], ",")
			end_coords = int_split(coords_list[i+1], ",")
			x_coords = sorted([start_coords[1], end_coords[1]])
			x_coords[1] += 1
			y_coords = sorted([start_coords[0], end_coords[0]])
			y_coords[1] += 1
			if is_test:
				y_coords = [a - 400 for a in y_coords]
			for x in range(*x_coords):
				for y in range(*y_coords):
					field.get(x, y).value = "#"

	all_rocks = [r for r in field.gen_cells(filterer=lambda c: c.value == "#")]
	floor_depth = max(r.x for r in all_rocks) + 2
	for y in range(field.y_size):
		field.get(floor_depth, y).value = "#"
	
	sand_start = field.get(0, 100) if is_test else field.get(0, 500)
	fall_path = [sand_start]
	i = 0
	while True:
		curr = fall_path[-1]
		if not (fall := field.get(curr.x+1, curr.y)).value:
			fall_path.append(fall)
		elif not (fall := field.get(curr.x+1, curr.y-1)).value:
			fall_path.append(fall)
		elif not (fall := field.get(curr.x+1, curr.y+1)).value:
			fall_path.append(fall)
		else: 
			if curr == sand_start:
				return i + 1
			curr.value = "o"
			fall_path.pop()
			i += 1
