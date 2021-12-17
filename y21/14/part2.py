from typing import List
import itertools as it

def run(input_data: List[str]) -> int:
	start_string = input_data[0]
	all_letters = set(list(start_string))

	rules = {}
	for i in range(2, len(input_data)):
		rule, insert = input_data[i].split(" -> ")
		rules[rule] = insert
		all_letters.add(insert)

	pairs = {}
	for i in range(1, len(start_string)):
		if pairs.get(f"{start_string[i-1]}{start_string[i]}"):
			pairs[f"{start_string[i-1]}{start_string[i]}"] += 1
		else:
			pairs[f"{start_string[i-1]}{start_string[i]}"] = 1

	for _ in range(40):
		new_pairs = {}
		for p, c in pairs.items():
			if p in rules.keys():
				insert = rules[p]
				if new_pairs.get(f"{p[0]}{insert}"):
					new_pairs[f"{p[0]}{insert}"] += c
				else:
					new_pairs[f"{p[0]}{insert}"] = c
				if new_pairs.get(f"{insert}{p[1]}"):
					new_pairs[f"{insert}{p[1]}"] += c
				else:
					new_pairs[f"{insert}{p[1]}"] = c
			else: new_pairs[p] = c
		pairs = new_pairs

	letters = {}
	for l in all_letters:
		letters[l] = 0
	letters[start_string[len(start_string)-1]] = 1
	for p, c in pairs.items():
		letters[p[0]] += c

	return max(v for v in letters.values()) - min(v for v in letters.values())
