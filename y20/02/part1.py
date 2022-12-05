from typing import List

def is_valid_password(minimum: int, maximum: int, letter: str, password: str) -> bool:
	instances = password.count(letter)
	if instances < minimum:
		return False
	if instances > maximum:
		return False
	return True

def run(input_data: List[str], **kwargs) -> int:
	total_valid: int = 0
	for datum in input_data:
		range_seg, char_seg, password = datum.split()
		min_str, max_str = range_seg.split('-')
		letter: str = char_seg[0]
		if is_valid_password(int(min_str), int(max_str), letter, password):
			total_valid += 1
	return total_valid