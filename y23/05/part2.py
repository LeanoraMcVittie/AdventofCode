from typing import List

def run(input_data: List[str], **kwargs) -> int:
	seed_line = [int(s) for s in input_data[0].split(": ")[1].split()]
	curr_map = []
	for i in range(0, len(seed_line), 2):
		curr_map.append((seed_line[i], seed_line[i+1]))
	new_map = []
	i = 1
	for _ in range(7):
		i += 2
		while i < len(input_data) and len(input_data[i]) > 0:
			dest, source, r = (int(s) for s in input_data[i].split())
			remove = []
			for s, l in curr_map:
				if s < source + r and source < s + l:
					start = max(s, source)
					total = min(s + l, source + r) - start
					remove.append((start, total))
					new_map.append((dest + (start - source), total))
			for start, total in remove:
				while (
					to_fix := [
						(s, l) for s, l in curr_map 
						if s < start + total and start < s + l
					]
				):
					s, l = to_fix[0]
					curr_map.remove((s, l))
					if diff := start - s > 0:
						curr_map.append((s, diff))
					if diff := (s + l) - (start + total) > 0:
						curr_map.append((start + total, diff))
			i += 1
		new_map.extend(curr_map)
		curr_map = new_map
		new_map = []

	return min(s for s, _ in curr_map)