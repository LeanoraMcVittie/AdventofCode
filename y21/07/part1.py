from typing import List

def run(input_data: List[str]) -> int:
	crabs = [int(c) for c in input_data[0].split(",")]
	crabs.sort(reverse=True)
	max_crab = crabs[0] + 1
	
	fuel_consumed_down = [0] * max_crab
	crab_index = 0
	for i in range(max_crab-2, -1, -1):
		while crab_index < len(crabs) and i < crabs[crab_index]:
			crab_index += 1
		fuel_consumed_down[i] = fuel_consumed_down[i+1] + crab_index

	crabs.sort()
	fuel_consumed_up = [0] * max_crab
	crab_index = 0
	for i in range(1, max_crab):
		while crab_index < len(crabs) and i > crabs[crab_index]:
			crab_index += 1
		fuel_consumed_up[i] = fuel_consumed_up[i-1] + crab_index

	total_fuel_consumed = [fuel_consumed_up[i] + fuel_consumed_down[i] for i in range(0, max_crab)]
	return min(total_fuel_consumed)
