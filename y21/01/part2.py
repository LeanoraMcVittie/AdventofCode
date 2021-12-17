from typing import List

def run(input_data: List[str]) -> str:
	increasing: int = 0
	current: int = 200000
	for i in range(2, len(input_data)):
		new = int(input_data[i]) + int(input_data[i-1]) + int(input_data[i-2])
		if new > current:
			increasing += 1
		current = new
	return str(increasing)