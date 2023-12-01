from typing import List

def run(input_data: List[str], **kwargs) -> int:
	frequency = 0
	frequencies = {frequency}
	while True:
		for f in input_data:
			frequency += int(f)
			if frequency in frequencies: return frequency
			frequencies.add(frequency)