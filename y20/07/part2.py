from typing import List
from utils.bag_tree import BagTree

def run(input_data: List[str], **kwargs) -> int:
	bag_tree = BagTree()
	for datum in input_data:
		bag_tree.parse_rule(datum)
	return len(bag_tree.get_children_contained("shiny gold"))
