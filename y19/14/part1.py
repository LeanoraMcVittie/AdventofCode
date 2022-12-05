from typing import List, Tuple
from math import ceil


class Reaction:
	def __init__(self, amt: int, reagents: List[Tuple["Chemical", int]]) -> None:
		self.total_reactions = 0
		self.amt_created = amt
		self.reagents = reagents

	def react(self) -> int:
		self.total_reactions += 1
		for c, q in self.reagents:
			c.request(q)
		return self.amt_created


class Chemical:
	def __init__(self, name: str) -> None:
		self.name = name
		self.unused = 0
		self.reaction = None
		self.total_requested = 0

	def set_reaction(self, reaction: Reaction) -> None:
		self.reaction = reaction

	def request(self, amount: int) -> None:
		self.total_requested += amount
		while self.unused < amount:
			amt_created = self.reaction.react()
			self.unused += amt_created
		self.unused -= amount


class Ore(Chemical):
	unused = 0

	def __init__(self) -> None:
		self.total_requested = 0
		self.name = "ORE"

	def request(self, amount: int) -> None:
		self.total_requested += amount


def run(input_data: List[str], **kwargs) -> int:
	chemicals_by_name = {"ORE": Ore()}
	for datum in input_data:
		reagents_string, chemical_str = datum.split(" => ")
		reaction_reagents = [
			(
				chemicals_by_name.setdefault(
					ingredient.split(" ")[1], Chemical(ingredient.split(" ")[1])
				),
				int(ingredient.split(" ")[0])
			)
			for ingredient in reagents_string.split(", ")
		]
		amt, chem = chemical_str.split(" ")
		chemicals_by_name.setdefault(chem, Chemical(chem)).set_reaction(Reaction(int(amt), reaction_reagents))
	chemicals_by_name.get("FUEL").request(1)
	return chemicals_by_name.get("ORE").total_requested
