from typing import List


# 51316
def run(input_data: List[str], **kwargs) -> int:
	total = 0
	for datum in input_data:
		added_fuel = int(int(datum)/3) - 2
		while added_fuel > 0:
			total += added_fuel
			added_fuel = int(added_fuel/3) - 2
	return total
