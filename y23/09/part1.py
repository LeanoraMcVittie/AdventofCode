from typing import List
from itertools import pairwise

def run(input_data: List[str], **kwargs) -> int:
	total = 0
	for datum in input_data:
		history = [[int(i) for i in datum.split()]]
		differences = [h2 - h1 for h1, h2 in pairwise(history[-1])]
		while any(d != 0 for d in differences):
			history.append(differences)
			differences = [h2 - h1 for h1, h2 in pairwise(history[-1])]
		history.append(differences)

		next = 0
		while len(history) > 1:
			history.pop(-1)
			next = history[-1][-1] + next
		total += next
	return total

