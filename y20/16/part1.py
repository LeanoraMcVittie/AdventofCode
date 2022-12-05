from typing import List


class Range:
	minimum: int
	maximum: int

	def __init__(self, range_str: str) -> None:
		minimum, maximum = range_str.split("-")
		self.minimum = int(minimum)
		self.maximum = int(maximum)

	def is_in_range(self, test: int) -> bool:
		return test >= self.minimum and test <= self.maximum


class Rule:
	name: str
	ranges: List[Range]

	def __init__(self, rule: str) -> None:
		self.name, ranges_str = rule.split(": ")
		self.ranges = [Range(range_str) for range_str in ranges_str.split(" or ")]

	def is_valid(self, test: int) -> bool:
		return any(r.is_in_range(test) for r in self.ranges)


def run(input_data: List[str], **kwargs) -> int:
	rules: List[Rule] = []
	i = 0
	while input_data[i] != "":
		rules.append(Rule(input_data[i]))
		i += 1
	my_ticket = [int(elem) for elem in input_data[i+2].split(",")]

	error_rate = 0
	for i in range(i+5, len(input_data)):
		for elem in input_data[i].split(","):
			if all(not rule.is_valid(int(elem)) for rule in rules):
				error_rate += int(elem)
	return error_rate

