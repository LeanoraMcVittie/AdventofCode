from typing import List
from utils.field.two_d import Coord
from itertools import combinations

def run(input_data: List[str], **kwargs) -> int:
	expanded_ver = []
	for row in input_data:
		if set(row) == {"."}:
			expanded_ver.append(row)
		expanded_ver.append(row)
	
	expanded = [""] * len(expanded_ver)	
	for i, _ in enumerate(expanded_ver[0]):
		new = []
		for j, row in enumerate(expanded):
			row += expanded_ver[j][i]
			new.append(row)
		expanded = new
		new = []
		if all(row[i] == "." for row in expanded_ver):
			for row in expanded:
				row += "."
				new.append(row)
				expanded = new

	galaxies = []
	for i in range(len(expanded)):
		for j in range(len(expanded[0])):
			if expanded[i][j] == "#":
				galaxies.append(Coord(i, j))

	total = 0
	for g1, g2 in combinations(galaxies, 2):
		total += abs(g1.x - g2.x) + abs(g1.y - g2.y)
	return total