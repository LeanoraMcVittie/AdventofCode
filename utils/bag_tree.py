from __future__ import annotations
from typing import Dict, List

class CountableBag:
	bag: Bag
	num: int

	def __init__(self, bag: Bag, num: int) -> None:
		self.bag = bag 
		self.num = num

class Bag:
	color: str
	parents: List[Bag]
	children: List[CountableBag]

	def __init__(self, color: str) -> None:
		self.color = color
		self.parents = []
		self.children = []

	def add_parent(self, parent: Bag, count: int) -> None:
		self.parents.append(parent)
		parent.children.append(CountableBag(self, count))


class BagTree:
	bags_by_color: Dict[str, Bag]

	def __init__(self) -> None:
		self.bags_by_color = {}

	def _get_or_make_bag(self, color: str) -> Bag:
		bag = self.bags_by_color.get(color)
		if not bag:
			bag = Bag(color)
			self.bags_by_color[color] = bag 
		return bag

	def _add_rule(
		self, 
		parent_color: str, 
		child_color: Optional[str] = None, 
		count: Optional[int] = None
	) -> None:
		parent_bag = self._get_or_make_bag(parent_color)
		if not child_color:
			return
		child_bag = self._get_or_make_bag(child_color)
		child_bag.add_parent(parent_bag, count)

	def parse_rule(self, rule: str) -> None:
		parent, children = rule.split(" contain ")
		parent = parent.replace(" bags", "")
		children = children.split(",")
		children = [
			child.strip().replace(".", "").replace(" bags", "").replace(" bag", "")
			for child in children
		]
		for child in children:
			if child.strip() == "no other":
				self._add_rule(parent)
				continue
			count, child_color = child.split(" ", 1)
			self._add_rule(parent, child_color, int(count))

	def get_possible_wrapper_bags(self, color: str) -> List[Bag]:
		child_bags: List[Bag] = [self.bags_by_color[color]]
		all_bags: List[Bag] = []
		while child_bags:
			child_bags = [parent for child in child_bags for parent in child.parents]
			all_bags.extend(child_bags)

		unique_bags: List[Bag] = []
		for bag in all_bags:
			if bag not in unique_bags:
				unique_bags.append(bag)
		return unique_bags

	def get_children_contained(self, color: str) -> List[Bag]:
		parent_bags: List[Bag] = [self.bags_by_color[color]]
		all_bags: List[Bag] = []
		while parent_bags:
			parent_bags = [
				cchild.bag 
				for parent in parent_bags 
				for cchild in parent.children 
				for i in range(0, cchild.num)
			]
			all_bags.extend(parent_bags)
		return all_bags
