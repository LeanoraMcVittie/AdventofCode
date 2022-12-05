from typing import List

def char_val(c: str) -> int:
	if c.islower():
		return ord(c) - 96
	return ord(c) - 38

def run(input_data: List[str], **kwargs) -> int:
	count = 0
	for i in range(0, len(input_data), 3):
		one = input_data[i]
		two = input_data[i+1]
		three = input_data[i+2]
		for c in one:
			if c in two and c in three:
				count += char_val(c)
				break
	return count
