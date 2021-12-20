from typing import List, Tuple
import itertools as it
from utils.math import lcm


def find_cycle(positions: Tuple[int, int, int, int]) -> int:
	i = 0
	seen_states = {}
	velocities = [0,0,0,0]
	while tuple(velocities) not in seen_states.get(tuple(positions), []):
		i += 1
		seen_states.setdefault(tuple(positions), []).append(tuple(velocities))
		for a, b in it.combinations(range(len(positions)), 2):
			if positions[a] > positions[b]:
				velocities[a] -= 1
				velocities[b] += 1
			elif positions[a] < positions[b]:
				velocities[a] += 1
				velocities[b] -= 1
		new_positions = []
		for m in range(len(positions)):
			new_positions.append(positions[m] + velocities[m])
		positions = new_positions
	return i


def run(input_data: List[str]) -> int:
	positions = [[] for _ in range(3)]
	for datum in input_data:
		x, y, z = datum[1:-1].split(", ")
		_, x = x.split("=")
		_, y = y.split("=")
		_, z = z.split("=")
		positions[0].append(int(x))
		positions[1].append(int(y))
		positions[2].append(int(z))
	return lcm([find_cycle(tuple(p)) for p in positions])
