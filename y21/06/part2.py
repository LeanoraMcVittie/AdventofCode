from typing import List

def run(input_data: List[str]) -> int:
	lanternfish = [int(datum) for datum in input_data[0].split(",")]
	lanternfish_counts = [lanternfish.count(i) for i in range(0, 9)]
	for i in range(0, 256):
		spawners = lanternfish_counts.pop(0)
		lanternfish_counts[6] += spawners
		lanternfish_counts.append(spawners)
	return sum(lanternfish_counts)
