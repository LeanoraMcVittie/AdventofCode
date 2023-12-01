from typing import List

def run(input_data: List[str], **kwargs) -> int:
	count_twos = 0
	count_threes = 0
	for id in input_data:
		letter_counts = {}
		for l in id:
			letter_counts[l] = 1 + letter_counts.get(l, 0)
		# print(id)
		# print(letter_counts)
		# print()
		counts = set(letter_counts.values())
		if 2 in counts: count_twos += 1
		if 3 in counts: count_threes += 1
	return count_twos * count_threes
