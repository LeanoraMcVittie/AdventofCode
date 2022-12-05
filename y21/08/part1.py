from typing import List


def run(input_data: List[str], **kwargs) -> int:
	count = 0
	for datum in input_data:
		inputs, outputs = datum.split(" | ")
		outputs = outputs.split(" ")
		for output in outputs:
			x = len(output)
			if x == 2 or x == 3 or x == 4 or x == 7:
				count += 1
	return count

