from typing import List

def phase(input_list: List[int]) -> List[int]:
	length = len(input_list)
	output_list = [0]*length

	i = length - 1
	running_pos = 0
	running_neg = 0
	while 5 * i + 4 > length:
		running_pos += input_list[i]
		running_pos -= sum(input_list[(2 * i) + 1:(2 * i) + 3])
		running_neg += sum(input_list[(3 * i) + 2:(3 * i) + 5])
		running_neg -= sum(input_list[(4 * i) + 3:(4 * i) + 7])
		output_list[i] = abs(running_pos - running_neg) % 10
		i -= 1

	while i >= 0:
		pos = sum(sum(input_list[i+a::(i + 1) * 4]) for a in range(i + 1))
		neg = sum(sum(input_list[(3 * i) + 2 + a::(i + 1) * 4]) for a in range(i + 1))
		output_list[i] = abs(pos - neg) % 10
		i -= 1
	return output_list

def run(input_data: List[str]) -> int:
	input_list = [int(e) for e in input_data[0]]
	for _ in range(100):
		input_list = phase(input_list)
	return str.join('', [str(e) for e in input_list[:8]])
