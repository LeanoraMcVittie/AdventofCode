from typing import List
from itertools import combinations, zip_longest

def num_placements(line: str) -> int:
	springs, arr = line.split()
	lengths = [int(a) for a in arr.split(",")]
	min_len = sum(lengths) + len(lengths) - 1
	chunks = [c for c in springs.split(".") if c != ""]
	chunk_lens = [len(c) for c in chunks]
	
	if (
		springs == min_len 
		or sum(chunk_lens) + len(chunk_lens) - 1 == min_len
	):
		return 1

	num_arr = 0
	extra_dots = sum(chunk_lens) + len(chunk_lens) - 1 - min_len
	extra_dot_buckets = len(lengths) + 1
	cond_springs = ".".join(chunks)
	for xlocs in combinations(range(extra_dots + extra_dot_buckets - 1), extra_dot_buckets - 1):
		option = ["."] * (extra_dots + extra_dot_buckets - 1)
		for xloc in xlocs:
			option[xloc] = "X"
		dot_distributions = "".join(option).split("X")
		distribution = ""
		for i, dots in enumerate(dot_distributions):
			distribution += dots
			if i < len(lengths):
				if i > 0: distribution += "."
				distribution += "#" * lengths[i]
		assert len(cond_springs) == len(distribution)
		if all(
			a == "?" or a == b
			for a, b 
			in zip_longest(cond_springs, distribution)
		): 
			num_arr += 1
	return num_arr


def run(input_data: List[str], **kwargs) -> int:
	num_arr = 0
	for line in input_data:
		qty = num_placements(line)
		print(f"{line}: {qty}")
		num_arr += qty
	return num_arr
			
		