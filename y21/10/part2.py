from typing import List

def parse_chunk(chunk: str) -> int:
	stack = []
	for i in range(len(chunk)):
		if chunk[i] == ")":
			if stack.pop(-1) != "(":
				return 0
		elif chunk[i] == "}":
			if stack.pop(-1) != "{":
				return 0
		elif chunk[i] == "]":
			if stack.pop(-1) != "[":
				return 0
		elif chunk[i] == ">":
			if stack.pop(-1) != "<":
				return 0
		else:
			stack.append(chunk[i])

	score = 0
	while len(stack) > 0:
		score *= 5
		score += {
			"(": 1,
			"[": 2,
			"{": 3,
			"<": 4
		}[stack.pop(-1)]
	return score

def run(input_data: List[str]) -> int:
	scores = [parse_chunk(datum) for datum in input_data]
	scores = [score for score in filter(lambda x: x != 0, scores)]
	scores.sort()
	return scores[int(len(scores)/2)]

