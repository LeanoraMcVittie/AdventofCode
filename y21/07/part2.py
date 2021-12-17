from typing import List


class Step:
	total_fuel_consumed: int
	fuel_consumed_in_step: int

	def __init__(self) -> None:
		self.total_fuel_consumed = 0
		self.fuel_consumed_in_step = 0

	def update(self, total_num_crabs, last_step) -> None:
		self.fuel_consumed_in_step = last_step.fuel_consumed_in_step + total_num_crabs
		self.total_fuel_consumed = last_step.total_fuel_consumed + self.fuel_consumed_in_step


def run(input_data: List[str]) -> int:
	crabs = [int(c) for c in input_data[0].split(",")]
	crabs.sort(reverse=True)
	max_crab = crabs[0] + 1
	
	steps_down = [Step() for i in range(max_crab)]
	crab_index = 0
	for i in range(max_crab-2, -1, -1):
		while crab_index < len(crabs) and i < crabs[crab_index]:
			crab_index += 1
		steps_down[i].update(crab_index, steps_down[i+1])

	crabs.sort()
	steps_up = [Step() for i in range(max_crab)]
	crab_index = 0
	for i in range(1, max_crab):
		while crab_index < len(crabs) and i > crabs[crab_index]:
			crab_index += 1
		steps_up[i].update(crab_index, steps_up[i-1])

	total_fuel_consumed = [
		steps_up[i].total_fuel_consumed + steps_down[i].total_fuel_consumed
		for i in range(max_crab)
	]
	return min(total_fuel_consumed)
