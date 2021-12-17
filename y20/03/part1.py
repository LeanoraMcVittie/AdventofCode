from typing import List

def run(input_data: List[str]) -> int:
	xloc: int = 3
	trees: int = 0
	input_data.pop(0)
	line_len = len(input_data[0]) - 1
	for datum in input_data:
		pos = xloc % line_len
		if datum[pos] == '#':
			trees += 1
		xloc += 3
	return trees