from typing import List
import itertools as it

def run(input_data: List[str], **kwargs) -> int:
	start_string = input_data[0]
	all_letters = set(list(start_string))

	rules = {}
	for i in range(2, len(input_data)):
		rule, insert = input_data[i].split(" -> ")
		rules[rule] = insert
		all_letters.add(insert)

	for _ in range(10):
		new_string = ""
		for i in range(1, len(start_string)):
			new_string += start_string[i-1]
			insert = rules[f"{start_string[i-1]}{start_string[i]}"]
			if insert:
				new_string += insert
		new_string += start_string[i]
		start_string = new_string

	return max(start_string.count(l) for l in all_letters) - min(start_string.count(l) for l in all_letters)
