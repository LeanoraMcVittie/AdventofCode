from typing import List
from itertools import zip_longest

GENERATIONS: int = 50000000000

def run(input_data: List[str], **kwargs) -> int:
	initial_str = input_data[0][15:]
	plant_locations = [idx for idx, pot in enumerate(initial_str) if pot == "#"]
	rules = []
	for rule in input_data[2:]:
		if rule[-1] == ".": continue # skip rules that don't result in a plant
		rules.append([idx - 2 for idx, pot in enumerate(rule[:5]) if pot == "#"])

	stable = False
	gens = 0
	while not stable:
		new_plant_locations = []
		for pot in range(plant_locations[0] - 2, plant_locations[-1] + 2):
			for rule in rules:
				for i in range(-2, 3):
					# ^ is xor operator
					if ((i in rule) ^ ((pot + i) in plant_locations)):
						break
				else:
					new_plant_locations.append(pot)
					break
		
		gens += 1
		if all(
			old and new and old + 1 == new 
			for old, new 
			in zip_longest(plant_locations, new_plant_locations)
		):
			stable = True

		plant_locations = new_plant_locations
	
	return sum(plant_locations) + (len(plant_locations) * (GENERATIONS - gens))
