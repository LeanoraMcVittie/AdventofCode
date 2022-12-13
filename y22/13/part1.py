from typing import List
import json

def check_order(left, right) -> bool:
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
		if (res := check_order(l, r)) is not None:
			return res
	if len(right) > len(left):
		return True
	return None

def run(input_data: List[str], **kwargs) -> int:
	count = 0
	for i in range(0, len(input_data), 3):
		first = json.loads(input_data[i])
		second = json.loads(input_data[i+1])

		if check_order(first, second):
			index = (i+2)//3 + 1
			count += index
	return count
