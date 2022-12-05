from typing import List

PREAMBLE_LENGTH = 25

def can_sum(total: int, values: List[str]) -> bool:
	for i in range(0, len(values)):
		for j in range(i+1, len(values)):
			if values[i] + values[j] == total:
				return True
	return False


def get_unsummable(input_data: List[int]) -> int:
	for i in range(PREAMBLE_LENGTH, len(input_data)):
		if not can_sum(
			input_data[i], [input_data[j] for j in range(i-PREAMBLE_LENGTH, i)]
		):
			return i
	return -1

def run(input_data: List[str], **kwargs) -> int:
	input_data = [int(datum) for datum in input_data]
	unsummable_index = get_unsummable(input_data)
	unsummable = input_data[unsummable_index]
	for i in range(0, unsummable_index):
		for j in range(i+1, unsummable_index):
			test_sum = sum([input_data[k] for k in range(i, j+1)])
			if test_sum == unsummable:
				values: List[int] = [input_data[k] for k in range(i, j+1)]
				return min(values) + max(values)
	return -1
