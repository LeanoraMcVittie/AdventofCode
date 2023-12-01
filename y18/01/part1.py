from typing import List

def run(input_data: List[str], **kwargs) -> int:
	frequency = 0
	for f in input_data:
		frequency += int(f)
	return frequency
