from typing import List, Set

class Allergen:
	def __init__(self, name: str) -> None:
		self.name = name
		self.possible_ingredients: Set[str] = None

	def update_ingredients(self, ingredients: List[str]) -> None:
		if self.possible_ingredients is None:
			self.possible_ingredients = set(ingredients)
		else:
			self.possible_ingredients = self.possible_ingredients.intersection(ingredients)


def run(input_data: List[str], **kwargs) -> int:
	allergens_dict = {}
	all_ingredients = {} 
	for datum in input_data:
		ingredients, allergens = datum.split(" (contains ")
		for allergen in allergens[:-1].split(", "):
			allergens_dict.setdefault(allergen, Allergen(allergen)).update_ingredients(ingredients.split(" "))
		for ingredient in ingredients.split(" "):
			all_ingredients.setdefault(ingredient, 0)
			all_ingredients[ingredient] += 1
	no_allergen_ingredients = list(all_ingredients.keys())
	for allergen in allergens_dict.values():
		for ingredient in allergen.possible_ingredients:
			if ingredient in no_allergen_ingredients:
				no_allergen_ingredients.remove(ingredient)
	return sum(all_ingredients[i] for i in no_allergen_ingredients)
