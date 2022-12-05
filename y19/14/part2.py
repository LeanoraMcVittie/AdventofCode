from typing import List, Tuple
from math import ceil


class OutOfOre(Exception):
	pass


class Reaction:
	def __init__(self, amt: int, reagents: List[Tuple["Chemical", int]]) -> None:
		self.total_reactions = 0
		self.amt_created = amt
		self.reagents = reagents

	def react(self, to_create: int) -> int:
		num_reactions = ceil(to_create / self.amt_created)
		for c, q in self.reagents:
			c.request(q * num_reactions)
		self.total_reactions += num_reactions
		return self.amt_created * num_reactions


class Chemical:
	def __init__(self, name: str) -> None:
		self.name = name
		self.unused = 0
		self.reaction = None
		self.total_requested = 0

	def set_reaction(self, reaction: Reaction) -> None:
		self.reaction = reaction

	def request(self, amount: int) -> None:
		if self.unused < amount:
			self.unused += self.reaction.react(amount - self.unused)
		self.total_requested += amount
		self.unused -= amount


class Ore(Chemical):
	START_AMOUNT: int = 1000000000000
	unused: int = 0
	name: str = "ORE"

	def __init__(self) -> None:
		self.total_requested = 0

	def request(self, amount: int) -> None:
		if self.total_requested + amount > Ore.START_AMOUNT:
			raise OutOfOre()
		self.total_requested += amount


def run(input_data: List[str], **kwargs) -> int:
	ore = Ore()
	chemicals_by_name = {ore.name: ore}
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

	fuel = chemicals_by_name.get("FUEL")
	fuel.request(1)
	max_ore_per_fuel = ore.total_requested

	while True:
		fuel_to_request = int((ore.START_AMOUNT - ore.total_requested) / max_ore_per_fuel) or 1
		try: fuel.request(fuel_to_request)
		except OutOfOre: return fuel.total_requested
