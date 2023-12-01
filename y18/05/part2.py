from typing import List

def polymer_reduction(polymer: str) -> int:
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

def run(input_data: List[str], **kwargs) -> int:
	polymer = input_data[0]
	shortest_len = len(polymer)
	shortest_letter = "a"
	for l in "abcdefghijklmnopqrstuvwxyz":
		reduced_len = polymer_reduction(
			polymer.replace(l, "").replace(l.upper(), "")
		)
		if reduced_len < shortest_len:
			shortest_len = reduced_len
			shortest_letter = l
	
	print(shortest_letter)
	return shortest_len