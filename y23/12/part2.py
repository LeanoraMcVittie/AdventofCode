from typing import List
from functools import cache

@cache
def num_placements(springs: str, arr: str) -> int:
	orig_springs = springs
	segments = [int(a) for a in arr.split(",")]
	min_len = sum(segments) + len(segments) - 1

	# base case
	if min_len > len(springs): 
		return 0

	counter = 0
	piece_size = segments[0]
	while len(springs) >= min_len:
		chunks = springs.split(".")
		chunk = chunks[0]

		if "#" in chunk	and len(chunk) < piece_size:
			# chunk is too small to fit the next piece
			# no more valid configurations down this route
			break
		
		for i in range(1 + len(chunk) - piece_size):
			# iterate through all positions this piece could hold
			# within this chunk
			if i > 0 and chunk[i - 1] == "#":
				# we have skipped a known broken piece
				# there are no more valid positions within this chunk
				break
			if i + piece_size < len(chunk) and chunk[i + piece_size] == "#":
				# the spring immediately after the end of this
				# position must be in the piece. This position
				# isn't valid, but the next one might be
				continue

			if len(segments) == 1:
				if "#" in springs[piece_size + i:]:
					# there's a broken spring that isn't covered yet
					continue
				counter += 1
			else:
				counter += num_placements(
					springs[piece_size + i + 1:].strip("."), 
					",".join(str(s) for s in segments[1:])
				)
		if "#" in chunk:
			# this segment must be in this chunk
			# do not try to process further chunks
			break
		springs = springs[len(chunk) + 1:]
	return counter


def run(input_data: List[str], **kwargs) -> int:
	num_arr = 0
	for line in input_data:
		springs, arr = line.split()
		springs = "?".join([springs] * 5)
		arr = ",".join([arr] * 5)
		chunks = [c for c in springs.split(".") if c != ""]
		placements = num_placements(".".join(chunks), arr)
		num_arr += placements

	return num_arr
			
		