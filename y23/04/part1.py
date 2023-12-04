from typing import List


def run(input_data: List[str], **kwargs) -> int:
	total = 0
	for line in input_data:
		_, nums = line.split(": ")
		wins, have = nums.split(" | ")
		winning_nums = set(wins.split())
		have_nums = set(have.split())
		num_matches = len(winning_nums.intersection(have_nums))
		if num_matches > 0:
			total += 2 ** (num_matches - 1)
	return total