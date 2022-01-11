from typing import List
from datetime import datetime


def phase(input_list: List[int], index: int) -> List[int]:
	length = len(input_list)
	output_list = [0]*length
	i = length - 1
	running_pos = 0
	running_neg = 0
	for i in range(length-1, index-1, -1):
		idx = i
		while idx < length:
			running_pos += input_list[idx]
			running_pos -= sum(input_list[(2 * idx) + 1:(2 * idx) + 3])
			running_neg += sum(input_list[(3 * idx) + 2:(3 * idx) + 5])
			running_neg -= sum(input_list[(4 * idx) + 3:(4 * idx) + 7])
			idx += i + 1
		output_list[i] = abs(running_pos - running_neg) % 10
	return output_list


def run(input_data: List[str]) -> int:
	if len(input_data[0]) == 32: return
	input_list = [int(e) for e in input_data[0]] * 10000
	index = int(input_data[0][:7])
	for i in range(100):
		start = datetime.now()
		input_list = phase(input_list, index)
		end = datetime.now()
		print(f"{i}: {end-start}")
	return str.join('', [str(e) for e in input_list[index:index+8]])
