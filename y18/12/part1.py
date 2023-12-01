from typing import List

GENERATIONS: int = 20

def run(input_data: List[str], **kwargs) -> int:
	initial_str = input_data[0][15:]
	plant_locations = [idx for idx, pot in enumerate(initial_str) if pot == "#"]
	rules = []
	for rule in input_data[2:]:
		if rule[-1] == ".": continue
		rules.append([idx - 2 for idx, pot in enumerate(rule[:5]) if pot == "#"])

	for _ in range(GENERATIONS):
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
		plant_locations = new_plant_locations

	return sum(plant_locations)
