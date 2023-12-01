from typing import List

def run(input_data: List[str], **kwargs) -> int:
	heuristic = int(input_data[0])
	recipes = [3, 7]
	elves = [0, 1]

	while len(recipes) < heuristic + 10:
		recipe_sum = sum(recipes[e] for e in elves)
		if recipe_sum >= 10:
			recipes.append(1)
			recipe_sum -= 10
		recipes.append(recipe_sum)
		elves = [(e + recipes[e] + 1) % len(recipes) for e in elves]
	return "".join([str(r) for r in recipes[heuristic:heuristic+10]])
	
