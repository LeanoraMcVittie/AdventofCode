from typing import List


# 34241
def run(input_data: List[str], **kwargs) -> int:
	total = 0
	for datum in input_data:
		total += int(int(datum)/3) - 2
	return total
