from typing import List

def run(input_data: List[str], **kwargs) -> int:
	polymer = input_data[0]
	i = 0
	while i < len(polymer) - 1:
		if (
			polymer[i].upper() == polymer[i+1].upper()
			and polymer[i] != polymer[i+1]
		):
			polymer = polymer[:i] + polymer[i+2:]
			i -= 1
			continue
		i += 1
	return len(polymer)
