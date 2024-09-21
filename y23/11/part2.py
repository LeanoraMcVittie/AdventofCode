from typing import List
from utils.field.two_d import Coord
from itertools import combinations

def run(input_data: List[str], **kwargs) -> int:
	galaxies = []
	for i in range(len(input_data)):
		for j in range(len(input_data[0])):
			if input_data[i][j] == "#":
				galaxies.append(Coord(i, j))
	
	x_to_expand = []
	for i in range(len(input_data)):
		if not any(g.x == i for g in galaxies):
			x_to_expand.append(i)
	
	y_to_expand = []
	for i in range(len(input_data[0])):
		if not any(g.y == i for g in galaxies):
			y_to_expand.append(i)

	total = 0
	for g1, g2 in combinations(galaxies, 2):
		x1 = g1.x + (999999 * len([x for x in x_to_expand if x < g1.x]))
		x2 = g2.x + (999999 * len([x for x in x_to_expand if x < g2.x]))
		y1 = g1.y + (999999 * len([y for y in y_to_expand if y < g1.y]))
		y2 = g2.y + (999999 * len([y for y in y_to_expand if y < g2.y]))
		total += abs(x1 - x2) + abs(y1 - y2)
	return total