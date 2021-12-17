from typing import List
from utils.math import product

def evaluate(expression: str) -> int:
	peren_count = 0
	final_expression = ""
	start_sub_expr = None
	for i in range(len(expression)):
		if expression[i] == "(":
			peren_count += 1
			if peren_count == 1:
				start_sub_expr = i+1
		elif expression[i] == ")":
			peren_count -= 1
			if peren_count == 0:
				final_expression += str(evaluate(expression[start_sub_expr:i]))
		elif peren_count == 0:
			final_expression += expression[i]
	
	elems = final_expression.split(" ")
	all_mults = []
	mini_sum = int(elems[0])
	for i in range(2, len(elems), 2):
		if elems[i-1] == "+":
			mini_sum += int(elems[i])
		elif elems[i-1] == "*":
			all_mults.append(mini_sum)
			mini_sum = int(elems[i])
		else:
			raise Exception("unexpected format")
	all_mults.append(mini_sum)
	return product(all_mults)


def run(input_data: List[str]) -> int:
	return sum(evaluate(datum) for datum in input_data)


