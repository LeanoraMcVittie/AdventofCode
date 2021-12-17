from typing import List

def run(input_data: List[str]) -> str:
	increasing: int = 0
	current: int = int(input_data[0])
	for datum in input_data:
		if int(datum) > current:
			increasing += 1
		current = int(datum)
	return str(increasing)