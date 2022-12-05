from typing import List

def char_val(c: str) -> int:
	if c.islower():
		return ord(c) - 96
	return ord(c) - 38

def run(input_data: List[str], **kwargs) -> int:
	count = 0
	for d in input_data:
		one = d[:len(d)//2]
		two = d[len(d)//2:]
		for c in one:
			if c in two:
				count += char_val(c)
				break
	return count
