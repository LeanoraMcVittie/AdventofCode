from typing import List, Tuple


def add_positions(start: Tuple[int, int], instruction: str) -> List[Tuple[int, int]]:
	direction = instruction[0]
	distance = int(instruction[1:])
	positions = []
	last_pos = start
	for _ in range(distance):
		last_pos = {
			"U": (last_pos[0], last_pos[1]+1),
			"D": (last_pos[0], last_pos[1]-1),
			"L": (last_pos[0]-1, last_pos[1]),
			"R": (last_pos[0]+1, last_pos[1]),
		}[direction]

		positions.append(last_pos)
	return positions


def get_line_positions(directions: str) -> List[Tuple[int, int]]:
	instructions = directions.split(",")
	positions = [(0,0)]
	for instruction in instructions:
		last_pos = positions[-1]
		positions.extend(add_positions(last_pos, instruction))
	return positions


def run(input_data: List[str], **kwargs) -> int:
	line1_positions = get_line_positions(input_data[0])
	line2_positions = get_line_positions(input_data[1])
	crossing_positions = set.intersection(set(line1_positions), set(line2_positions))
	crossing_positions.remove((0,0))
	min_distance = None
	for pos in crossing_positions:
		distance = line1_positions.index(pos) + line2_positions.index(pos)
		if min_distance is None or distance < min_distance:
			min_distance = distance
	return min_distance
