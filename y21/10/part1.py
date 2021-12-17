from typing import List

def parse_chunk(chunk: str) -> int:
	stack = []
	for i in range(len(chunk)):
		if chunk[i] == ")":
			if stack.pop(-1) != "(":
				return 3
		elif chunk[i] == "}":
			if stack.pop(-1) != "{":
				return 1197
		elif chunk[i] == "]":
			if stack.pop(-1) != "[":
				return 57
		elif chunk[i] == ">":
			if stack.pop(-1) != "<":
				return 25137
		else:
			stack.append(chunk[i])
	return 0

def run(input_data: List[str]) -> int:
	return sum([parse_chunk(datum) for datum in input_data])

