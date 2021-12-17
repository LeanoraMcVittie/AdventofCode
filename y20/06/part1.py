from typing import List

def run(input_data: List[str]) -> int:
	total: int = 0
	letters: List[str] = []
	for datum in input_data:
		if datum == "\n":
			total += len(set(letters))
			letters = []
			continue
		letters.extend(datum.strip())
	total += len(set(letters))
	return total
