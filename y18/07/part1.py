from typing import Dict, List

class Node:
	def __init__(self, name: str) -> None:
		self.name = name
		self.deps = []
		self.locked_prereqs = []

	def add_prereq(self, prereq: str) -> None:
		self.locked_prereqs.append(prereq)

	def add_dep(self, dep: "Node") -> None:
		self.deps.append(dep)

	def unlock(self) -> None:
		for dep in self.deps:
			dep.locked_prereqs.remove(self.name)
	

def run(input_data: List[str], **kwargs) -> int:
	nodes: Dict[str, Node] = {}
	for req in input_data:
		prereq = nodes.setdefault(req[5], Node(req[5]))
		dep = nodes.setdefault(req[36], Node(req[36]))
		dep.add_prereq(prereq.name)
		prereq.add_dep(dep)
	locked = sorted(list(nodes.keys()))
	order = ""
	while(locked):
		for l in locked:
			l = nodes.get(l)
			if not l.locked_prereqs:
				locked.remove(l.name)
				l.unlock()
				order += l.name
				break
	return order