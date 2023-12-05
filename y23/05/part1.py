from typing import List

def run(input_data: List[str], **kwargs) -> int:
	curr_map = [int(s) for s in input_data[0].split(": ")[1].split()]
	new_map = []
	i = 1
	for _ in range(7):
		i += 2
		while i < len(input_data) and len(input_data[i]) > 0:
			dest, source, r = (int(s) for s in input_data[i].split())
			remove = []
			for s in curr_map:
				if s >= source and s < source + r:
					remove.append(s)
					new_map.append(dest + (s - source))
			for s in remove:
				curr_map.remove(s)
			i += 1
		new_map.extend(curr_map)
		curr_map = new_map
		new_map = []

	return min(curr_map)