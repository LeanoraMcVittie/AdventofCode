from typing import Any

class Node:
	def __init__(self, value: Any) -> None:
		self.value = value
		self.children = []
		self.parents = []

	def add_child(self, child: "Node") -> None:
		self.children.append(child)
		child.parents.append(self)

	def get_ancestors(self) -> List["Node"]:
		ancestors = [self]
		[ancestors.extend(parent.get_ancestors()) for parent in self.parents]
		return ancestors

	def get_descendants(self) -> List["Node"]:
		descendants = [self]
		[descendants.extend(child.get_descendants()) for child in self.children]


class Tree:
	def __init__(self) -> None:
		self.nodes = {}
		self.root = None

	def _add_node(
		self, 
		node: "Node", 
		children: List["Node"] = None, 
		parents: List["Node"] = None,
	) -> None:
		self.nodes[node.value] = node
		[node.add_child(child) for child in children]
		[parent.add_child(node) for parent in parents]

	def add_child(self, **kwargs) -> None:
		raise Exception("add_child is unimplemented")

