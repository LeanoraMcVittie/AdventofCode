from typing import Dict, List, Optional
from math import lcm

class Node:
	name: str
	left: Optional["Node"]
	right: Optional["Node"]

	def __init__(self, n: str, l: Optional["Node"] = None, r: Optional["Node"] = None) -> None:
		self.name = n
		self.left = l
		self.right = r
	
	def set_right(self, r: "Node") -> None:
		self.right = r
	
	def set_left(self, l: "Node") -> None:
		self.left = l
	
	@property
	def is_start(self) -> bool:
		return self.name[2] == "A"
	
	@property
	def is_end(self) -> bool:
		return self.name[2] == "Z"


def run(input_data: List[str], **kwargs) -> int:
	instructions = input_data.pop(0)
	input_data.pop(0)
	node_map: Dict[str, Node] = {}
	for line in input_data:
		n = line[:3]
		l = line[7:10]
		r = line[12:15]

		left = node_map.get(l)
		if not left:
			left = Node(l)
			node_map[l] = left
		
		right = node_map.get(r)
		if not right:
			right = Node(r)
			node_map[r] = right

		if node := node_map.get(n):
			node.set_left(left)
			node.set_right(right)
		else:
			node_map[n] = Node(n, left, right)

	nodes = [n for n in node_map.values() if n.is_start]
	all_steps = [] 
	for n in nodes:
		curr_node = n
		ins = instructions
		steps = 0
		while not curr_node.is_end:
			steps += 1
			if len(ins) == 0:
				ins = instructions
			i = ins[0]
			ins = ins[1:]
			curr_node = curr_node.left if i == "L" else curr_node.right
		all_steps.append(steps)
	return lcm(*all_steps)
