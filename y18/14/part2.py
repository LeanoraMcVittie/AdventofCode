from typing import List

def run(input_data: List[str], **kwargs) -> int:
	digits = [int(i) for i in input_data[0]]
	recipes = [3, 7]
	elves = [0, 1]

	while recipes[-len(digits):] != digits:
		recipe_sum = sum(recipes[e] for e in elves)
		if recipe_sum >= 10:
			recipes.append(1)
			if recipes[-len(digits):] == digits:
				break
			recipe_sum -= 10
		recipes.append(recipe_sum)
		elves = [(e + recipes[e] + 1) % len(recipes) for e in elves]
	return len(recipes) - len(digits)
	
