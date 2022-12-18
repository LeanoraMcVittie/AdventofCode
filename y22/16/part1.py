from typing import Dict, List
import itertools 

class Valve:
	def __init__(self, name: str, flow_rate: int, tunnels: List[str]) -> None:
		self.name = name
		self.flow_rate = flow_rate
		self.tunnels = tunnels
	
	def find_useful_tunnels(self, useful_valves: List[str], av: Dict[str, "Valve"]) -> None:		
		self.useful_paths = {}
		for v in useful_valves:
			if self.name == v:
				continue
			self.useful_paths[v] = bfs(self, av[v], av)
			

def bfs(start: Valve, end: Valve, av: Dict[str, Valve]) -> int:
	paths = [[start]]
	while True:
		path = paths.pop(0)
		for t in path[-1].tunnels:
			if t == end.name:
				return len(path)
			if t not in [p.name for p in path]:
				paths.append(path + [av[t]])


def calculate_released(path: List[str], av: Dict[str, Valve]) -> int:
	moves_remaining = 30
	released = 0
	for a, b in itertools.pairwise(path):
		moves_remaining -= 1 + av[a].useful_paths[b]
		assert moves_remaining >= 0
		released += moves_remaining * av[b].flow_rate
	return released

def run(input_data: List[str], **kwargs) -> int:
	av = {}
	for d in input_data:
		parts = d.split()
		valve = parts[1]
		flow_rate = int(parts[4][5:-1])
		tunnels = [p.strip(",") for p in parts[9:]]
		av[valve] = Valve(valve, flow_rate, tunnels)
	
	useful_valves = [v.name for v in av.values() if v.flow_rate > 0]
	current_valve = "AA"
	
	for v in useful_valves + [current_valve]:
		av[v].find_useful_tunnels(useful_valves, av)

	total_moves = 30
	unfinished_paths = [([current_valve], 0)]
	max_released = 0
	count = 0
	while unfinished_paths:
		count += 1
		path, cost = unfinished_paths.pop()
		last_valve = path[-1]
		end = True
		for p, c in av[last_valve].useful_paths.items():
			if p in path or (nc := cost + c + 1) > total_moves:
				continue
			end = False
			unfinished_paths.append((path + [p], nc))
		if end and (released := calculate_released(path, av)) > max_released:
			max_released = released
	return max_released
