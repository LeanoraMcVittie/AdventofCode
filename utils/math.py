from typing import List

def product(vals: List[int]) -> int:
	product = 1
	for v in vals:
		product *= v
	return product
