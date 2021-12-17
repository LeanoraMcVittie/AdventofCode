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
	possible_positions: List[int]

	def __init__(self, rule: str) -> None:
		self.name, ranges_str = rule.split(": ")
		self.ranges = [Range(range_str) for range_str in ranges_str.split(" or ")]

	def is_valid(self, test: int) -> bool:
		return any(r.is_in_range(test) for r in self.ranges)

	def create_possible_positions(self, num_vals: int) -> None:
		self.possible_positions = list(range(num_vals))
		if None in self.possible_positions:
			import pdb; pdb.set_trace()


class Ticket:
	values: List[int]

	def __init__(self, values_str: str) -> None:
		self.values = [int(elem) for elem in values_str.split(",")]

	def is_valid(self, rules: List[Rule]) -> bool:
		for v in self.values:
			if all(not rule.is_valid(v) for rule in rules):
				return False
		return True

	def validate_rules(self, rules: List[Rule]) -> None:
		for i in range(len(self.values)):
			rules_left = [r for r in rules if i in r.possible_positions]
			for rule in rules_left:
				if not rule.is_valid(self.values[i]):
					rule.possible_positions.remove(i)


# This is not code I am proud of, but in the spirit of keeping it as I solved it...
def run(input_data: List[str]) -> int:
	rules: List[Rule] = []
	i = 0
	while input_data[i] != "":
		rules.append(Rule(input_data[i]))
		i += 1

	my_ticket = Ticket(input_data[i+2])
	[r.create_possible_positions(len(my_ticket.values)) for r in rules]

	valid_tickets: List[Ticket] = []
	for i in range(i+5, len(input_data)):
		ticket = Ticket(input_data[i])
		if not ticket.is_valid(rules):
			continue
		ticket.validate_rules(rules)

	valid_rules: List[Rule] = []
	while len(rules) > 0:
		for rule in rules:
			if len(rule.possible_positions) == 1:
				break
		else:
			raise ("broken")

		found_position = rule.possible_positions[0]
		if "departure" in rule.name:
			valid_rules.append(rule)
		rules.remove(rule)

		for rule in rules:
			if found_position in rule.possible_positions:
				rule.possible_positions.remove(found_position)


	assert all(len(r.possible_positions) == 1 for r in rules)
	departure_values = [my_ticket.values[rule.possible_positions[0]] for rule in valid_rules]
	product = 1
	for v in departure_values:
		product *= v
	return product