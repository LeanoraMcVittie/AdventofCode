from typing import List

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
	total = int(elems[0])
	for i in range(2, len(elems), 2):
		if elems[i-1] == "+":
			total += int(elems[i])
		elif elems[i-1] == "*":
			total *= int(elems[i])
		else:
			raise Exception("unexpected format")
	return total


def run(input_data: List[str]) -> int:
	return sum(evaluate(datum) for datum in input_data)


