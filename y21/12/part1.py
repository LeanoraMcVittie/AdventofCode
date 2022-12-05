from typing import Dict, List

class Cave:
	def __init__(self, name):
		self.name = name
		self.is_big = name.isupper()
		self.visited = False
		self.paths = []

	def add_connection(self, connection: "Cave"): 
		self.paths.append(connection)
		connection.paths.append(self)


def create_map(data: List[str]) -> Dict[str, Cave]:
	caves = {}
	for datum in data:
		cave1, cave2 = datum.split("-")
		caves.setdefault(cave1, Cave(cave1)).add_connection(caves.setdefault(cave2, Cave(cave2)))
	return caves

def traverse(start_cave: Cave) -> int:
	if start_cave.name == "end":
		return 1
	if not start_cave.is_big: start_cave.visited = True
	paths = 0
	for connection in start_cave.paths:
		if not connection.visited:
			paths += traverse(connection)
	start_cave.visited = False
	return paths


def run(input_data: List[str], **kwargs) -> int:
	caves = create_map(input_data)
	start_cave = caves["start"]
	return traverse(start_cave)
