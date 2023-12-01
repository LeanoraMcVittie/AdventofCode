from typing import List

alphabet = "abcdefghijklmnopqrstuvwxyz"

def run(input_data: List[str], **kwargs) -> int:
	total = 0
	for line in input_data:
		line = line.strip(alphabet)
		total += int(line[0]) * 10
		total += int(line[-1])
	return total
		
