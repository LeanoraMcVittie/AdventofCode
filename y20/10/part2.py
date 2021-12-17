from typing import List


def run(input_data: List[str]) -> int:
	data = [int(datum) for datum in input_data]
	data.append(max(data) + 3)
	data.append(0)
	data.sort()
	paths = [0 for i in range(0, len(data))]
	paths[0] = 1
	for i in range(1, len(data)):
		value = data[i]
		for j in range(1, 4):
			if i >= j and value - data[i-j] <= 3:
				paths[i] += paths[i-j]
	return max(paths)