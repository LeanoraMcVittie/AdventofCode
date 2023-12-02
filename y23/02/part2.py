from typing import List
from math import prod


def run(input_data: List[str], **kwargs) -> int:
	running_powers = 0
	for line in input_data:
		maximums = {}
		_, rounds = line.split(": ")
		for round in rounds.split("; "):
			totals = {"red": 0, "green": 0, "blue": 0}
			for c in round.split(", "):
				amt, color = c.split()
				totals[color] += int(amt)
			for k, v in totals.items():
				if maximums.get(k, 0) < v: maximums[k] = v
		running_powers += prod(maximums.values())
	return running_powers
	