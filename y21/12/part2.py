from typing import Dict, List

class Cave:
	def __init__(self, name):
		self.name = name
		self.is_big = name.isupper()
		self.visited = 0
		self.paths = []

	def add_connection(self, connection: "Cave"): 
		self.paths.append(connection)
		connection.paths.append(self)

class CaveMap:
	def __init__(self, data: List[str]):
		self.caves = {}
		self.visited_twice = False
		for datum in data:
			cave1, cave2 = datum.split("-")
			self.caves.setdefault(cave1, Cave(cave1)).add_connection(self.caves.setdefault(cave2, Cave(cave2)))

	def traverse(self, start_cave: Cave) -> int:
		if start_cave.name == "end": return 1

		if not start_cave.is_big: start_cave.visited += 1
		if start_cave.visited > 1: self.visited_twice = True

		paths = 0
		for connection in start_cave.paths:
			if connection.name == "start": continue
			if connection.visited > 0 and self.visited_twice: continue
			paths += self.traverse(connection)

		if start_cave.visited > 1:
			self.visited_twice = False
		start_cave.visited -= 1
		return paths

	def get_start(self) -> Cave:
		return self.caves["start"]

def run(input_data: List[str], **kwargs) -> int:
	caves = CaveMap(input_data)
	return caves.traverse(caves.get_start())
