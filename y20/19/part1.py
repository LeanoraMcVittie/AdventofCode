from typing import List
from itertools import product

class Rule:
	def __init__(self, sub_rules: List[str]) -> None:
		if sub_rules[0] == '"a"' or sub_rules[0] == '"b"':
			self.matching_strings = [sub_rules[0][1]]
		else:
			self.matching_strings = []
			try:
				self.sub_rules = [[int(r) for r in rule.split(" ")] for rule in sub_rules]
			except ValueError as e:
				print(sub_rules)
				raise e

	def get_matching_strings(self, rule_map: "RuleMap") -> List[str]:
		if not self.matching_strings:
			self.matching_strings = self.create_matching_strings(rule_map)
		return self.matching_strings

	def create_matching_strings(self, rule_map: "RuleMap") -> List[str]:
		matches = []
		for rule_set in self.sub_rules:
			match_rules = [""]
			for rule in rule_set:
				match_rules = [
					elem[0] +  elem[1] 
					for elem in product(
						match_rules, 
						rule_map.get(rule).get_matching_strings(rule_map)
					)
				]
			matches.extend(match_rules)
		return matches


class RuleMap:
	def __init__(self) -> None:
		self.rules = {}

	def get(self, rule: int) -> None:
		return self.rules[rule]

	def add_rule(self, rule_str: str) -> None:
		rule_id, sub_rules = rule_str.split(": ")
		self.rules[int(rule_id)] = Rule(sub_rules.split(" | "))


def run(input_data: List[str]) -> int:
	rule_map = RuleMap()
	i = 0
	while input_data[i] != "":
		rule_map.add_rule(input_data[i])
		i += 1

	valid_rules = rule_map.get(0).get_matching_strings(rule_map)
	i += 1
	count = 0
	while i < len(input_data):
		if input_data[i] in valid_rules:
			count += 1
		i += 1
	return count

