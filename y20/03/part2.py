from typing import List

def check_slope(right: int, down: int, data: List[str]) -> int:
	trees: int = 0
	xloc: int = right
	line_len: int = len(data[0]) - 1
	for i in range(down, len(data), down):
		pos = xloc % line_len
		if data[i][pos] == '#':
			trees += 1
		xloc += right
	return trees

def run(input_data: List[str], **kwargs) -> int:
	slope1: int = check_slope(1, 1, input_data)
	slope2: int = check_slope(3, 1, input_data)
	slope3: int = check_slope(5, 1, input_data)
	slope4: int = check_slope(7, 1, input_data)
	slope5: int = check_slope(1, 2, input_data)
	return slope1 * slope2 * slope3 * slope4 * slope5