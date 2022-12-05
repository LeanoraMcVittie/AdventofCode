from typing import List, Set

class Allergen:
	def __init__(self, name: str) -> None:
		self.name = name
		self.possible_ingredients: Set[str] = None
		self.ingredient = None
		self.requires_cleanup = False

	def update_ingredients(self, ingredients: List[str]) -> None:
		if self.possible_ingredients is None:
			self.possible_ingredients = set(ingredients)
		else:
			self.possible_ingredients = self.possible_ingredients.intersection(ingredients)
		if len(self.possible_ingredients) < 1:
			raise Exception(f"allergen without ingredient: {self.name}")
		if len(self.possible_ingredients) == 1:
			self.ingredient = list(self.possible_ingredients)[0]
			self.requires_cleanup = True

	def remove_ingredient(self, ingredient: str) -> None:
		if ingredient in self.possible_ingredients:
			self.possible_ingredients.remove(ingredient)
		if len(self.possible_ingredients) < 1:
			raise Exception(f"allergen without ingredient: {self.name}")
		if len(self.possible_ingredients) == 1:
			self.ingredient = list(self.possible_ingredients)[0]
			return True
		return False


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

	all_allergens = list(allergens_dict.values())
	to_cleanup = [allergen for allergen in all_allergens if allergen.requires_cleanup]
	for allergen in to_cleanup: all_allergens.remove(allergen)
	processed_allergens = []
	while len(to_cleanup) > 0:
		cleanup_allergen = to_cleanup.pop(0)

		remove_from_all_allergens = []
		for allergen in all_allergens:
			if allergen.remove_ingredient(cleanup_allergen.ingredient):
				remove_from_all_allergens.append(allergen)
				to_cleanup.append(allergen)
		
		for allergen in remove_from_all_allergens: all_allergens.remove(allergen)
		processed_allergens.append(cleanup_allergen)

	if len(all_allergens) != 0:
		raise Exception("allergens left unprocessed")

	processed_allergens.sort(key=lambda x: x.name)

	return str.join(",", [a.ingredient for a in processed_allergens])


