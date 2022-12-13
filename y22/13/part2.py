from typing import List
from utils.utils import merge_sort
import json

def is_smaller(left, right) -> bool:
	if isinstance(left, int):
		left = [left]
	if isinstance(right, int):
		right = [right]
	
	for i in range(len(left)):
		if i >= len(right):
			return False
		l = left[i]
		r = right[i]
		if isinstance(l, int) and isinstance(r, int):
			if l == r:
				continue
			return l < r
		if (res := is_smaller(l, r)) is not None:
			return res
	if len(right) > len(left):
		return True
	return None

def run(input_data: List[str], **kwargs) -> int:
	all_elements = [json.loads(d) for d in input_data if d]
	important_elements = [[[6]], [[2]]]
	all_elements.extend(important_elements)
	sorted_elements = merge_sort(all_elements, is_smaller)
	prod = 1
	for i, e in enumerate(sorted_elements):
		if e in important_elements:
			prod *= i + 1
	return prod