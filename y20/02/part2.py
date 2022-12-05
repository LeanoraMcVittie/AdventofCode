from typing import List

def is_valid_password(first_pos: int, second_pos: int, letter: str, password: str) -> bool:
	at_first_pos = password[first_pos-1] == letter
	at_second_pos = password[second_pos-1] == letter
	if at_first_pos and at_second_pos:
		return False
	if not at_first_pos and not at_second_pos:
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
