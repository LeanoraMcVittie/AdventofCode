from typing import List


PREAMBLE_LENGTH = 25


def can_sum(total: int, values: List[str]) -> bool:
	for i in range(0, len(values)):
		for j in range(i+1, len(values)):
			if values[i] + values[j] == total:
				return True
	return False


def run(input_data: List[str], **kwargs) -> int:
	for i in range(PREAMBLE_LENGTH, len(input_data)):
		if not can_sum(
			int(input_data[i]), [int(input_data[j]) for j in range(i-PREAMBLE_LENGTH, i)]
		):
			return int(input_data[i])
	return -1
