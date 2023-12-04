from typing import List


def run(input_data: List[str], **kwargs) -> int:
	num_each_card = [1] * len(input_data)
	for i, line in enumerate(input_data):
		_, nums = line.split(": ")
		wins, have = nums.split(" | ")
		winning_nums = set(wins.split())
		have_nums = set(have.split())
		for j in range(len(winning_nums.intersection(have_nums))):
			num_each_card[i + j + 1] += num_each_card[i]
	return sum(num_each_card)	
