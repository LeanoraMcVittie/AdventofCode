from typing import List
from collections import Counter
from functools import total_ordering
from itertools import zip_longest

CARDS = "J23456789TQKA"


@total_ordering
class Hand:
	value: str
	bid: int

	def __init__(self, v: str, b: str) -> None:
		self.value = v
		self.bid = int(b)
		self.type = self.get_type()
	
	def get_type(self) -> int:
		counted = Counter(self.value)
		jokers = counted.get("J")
		if jokers:
			del counted["J"]
			if len(counted) == 0:
				return 7
			common = counted.most_common(1)[0][0]
			counted[common] += jokers
		num_elems = len(counted)
		values = list(counted.values())
		if num_elems == 1:
			return 7
		elif 4 in values:
			return 6
		elif num_elems == 2:
			return 5
		elif num_elems == 3 and 3 in values:
			return 4
		elif num_elems == 3 and 2 in values and 1 in values:
			return 3
		elif num_elems == 4:
			return 2
		else:
			return 1
	
	def __eq__(self, other) -> bool:
		return (self.type, self.value) == (other.type, other.value)

	def __le__(self, other) -> bool:
		if self.type == other.type:
			for s, o in zip_longest(self.value, other.value):
				if s == o: continue
				return CARDS.index(s) < CARDS.index(o)
			return True
		return self.type < other.type

def run(input_data: List[str], **kwargs) -> int:
	hands = []
	for hand in input_data:
		hands.append(Hand(*hand.split()))
	hands.sort()
	
	total = 0
	for i, h in enumerate(hands):
		total += (i + 1) * h.bid
	return total
