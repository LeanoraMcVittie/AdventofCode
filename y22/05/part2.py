from typing import List

WHITESPACE = True
NUM_COLS = 9

def run(input_data: List[str], is_test) -> int:
	if is_test: num_cols = 3 
	else: num_cols = NUM_COLS
	stacks = {}
	j = 0
	for datum in input_data:
		j += 1
		if datum == "\n":
			break
		for i in range(1, (num_cols*4)+1, 4):
			if (c := datum[i]) != " " and c.isupper():
				stacks.setdefault((i//4)+1, []).append(c)
	
	for i in range(j, len(input_data)):
		datum = input_data[i]
		_, num, _, from_col, _, to_col = datum.split(" ")
		num, from_col, to_col = [int(a) for a in [num, from_col, to_col]]
		mov = stacks[from_col][:num]
		stacks[from_col] = stacks[from_col][num:]
		stacks[to_col] = mov + stacks[to_col]
	
	tops = ""
	for i in range(1, num_cols + 1):
		tops += stacks[i][0]
	return tops