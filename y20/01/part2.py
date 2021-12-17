from typing import List

def find_2020(values: List[int]) -> str:
	for i in range(0, len(values)):
		for j in range (i+1, len(values)):
			for k in range(j+1, len(values)):
				total = values[i] + values[j] + values[k]
				if total == 2020:
					return str(values[i] * values[j] * values[k])
				if total > 2020:
					break
	return "error"

def run(input_data: List[str]) ->  str:
	values = [int(val) for val in input_data]
	values.sort()
	return find_2020(values)
