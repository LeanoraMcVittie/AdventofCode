from typing import List
from itertools import product

class Rule:
	def __init__(self, value: int, sub_rules: List[str]) -> None:
		self.value = value
		if sub_rules[0] == '"a"' or sub_rules[0] == '"b"':
			self.matching_strings = [sub_rules[0][1]]
		else:
			self.matching_strings = []
			self.sub_rules = [[int(r) for r in rule.split(" ")] for rule in sub_rules]

	def get_matching_strings(self, rule_map: "RuleMap") -> List[str]:
		if not self.matching_strings:
			self.matching_strings = self.create_matching_strings(rule_map)
		return self.matching_strings

	def create_matching_strings(self, rule_map: "RuleMap") -> List[str]:
		matches = set()
		for rule_set in self.sub_rules:
			match_rules = [""]
			for rule in rule_set:
				if rule == 8 and rule == self.value:
					continue
				if rule == self.value:
					rule_additions = [" "]
				else:
					rule_additions = rule_map.get(rule).get_matching_strings(rule_map)
				match_rules = [
					elem[0] +  elem[1] 
					for elem in product(
						match_rules, 
						rule_additions,
					)
				]
			matches.update(match_rules)
		return list(matches)


class RuleMap:
	def __init__(self) -> None:
		self.rules = {}

	def get(self, rule: int) -> None:
		return self.rules[rule]

	def add_rule(self, rule_str: str) -> None:
		rule_id, sub_rules = rule_str.split(": ")
		rule_id = int(rule_id)
		if rule_id == 8:
			sub_rules = "42 | 42 8"
		elif rule_id == 11:
			sub_rules = "42 31 | 42 11 31"
		self.rules[rule_id] = Rule(rule_id, sub_rules.split(" | "))

	def matches_eleven(self, line: int) -> bool:
		for eleven_str in self.get(11).get_matching_strings(self):
			if line == eleven_str:
				return True
			if not " " in eleven_str:
				continue
			start_str, end_str = eleven_str.split(" ")
			if (
				line.startswith(start_str)
				and line.endswith(end_str)
				and self.matches_eleven(line[len(start_str):-len(end_str)])
			):
				return True
		return False

	def matches_zero(self, line: int) -> bool:
		for eight_str in self.get(8).get_matching_strings(self):
			if not line.startswith(eight_str):
				continue
			if (
				self.matches_zero(line[len(eight_str):])
				or self.matches_eleven(line[len(eight_str):])
			):
				return True
		return False


def run(input_data: List[str], **kwargs) -> int:
	rule_map = RuleMap()
	i = 0
	while input_data[i] != "":
		rule_map.add_rule(input_data[i])
		i += 1

	i += 1
	count = 0
	while i < len(input_data):
		if rule_map.matches_zero(input_data[i]):
			print(input_data[i])
			count += 1
		i += 1
	return count

