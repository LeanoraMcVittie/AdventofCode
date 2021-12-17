from typing import Dict, List

def run(input_data: List[str]) -> int:
	starters = [int(elem) for elem in input_data[0].split(",")]
	start_count = len(starters)
	counters: Dict[int, int] = {starters[i]: i+1 for i in range(0, start_count)}
	prev_number = starters[start_count-1]
	for i in range(start_count, 30000000):
		if prev_number in counters.keys():
			next_number = i - counters[prev_number]
		else:
			next_number = 0
		counters[prev_number] = i
		prev_number = next_number
	return prev_number
