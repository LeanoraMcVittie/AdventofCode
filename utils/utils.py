from typing import List

def get_input(module: str, prefix: str = "") -> List[str]:
	prefix += "_" if prefix else ""
	with open(f"{module}/{prefix}input.txt", 'r') as input_file:
		values: List[str] = input_file.readlines()
	return [v.strip() for v in values]

def is_valid_hex(hex: str) -> bool:
	try:
		int(hex, base=16)
	except ValueError:
		return False
	return True
