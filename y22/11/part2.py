from typing import List, Tuple
from utils.math import product


class Monkey:
	items: List[int]
	operation: str
	test: int 
	true_monkey: int 
	false_monkey: int 
	total_inspected: int

	def __init__(self, monkey_input: List[str]) -> None:
		_, items_str = monkey_input[0].split(":")
		self.items = [int(i) for i in items_str.strip().split(", ")]
		self.operation = monkey_input[1].split(" = ")[-1]
		self.test = int(monkey_input[2].split()[-1])
		self.true_monkey = int(monkey_input[3].split()[-1])
		self.false_monkey = int(monkey_input[4].split()[-1])
		self.total_inspected = 0

	def handle_item(self, mod_val: int) -> Tuple[int, int]:
		self.total_inspected += 1
		item = self.items.pop(0)
		res = eval(self.operation.replace("old", str(item)))
		res = res % mod_val
		if res % self.test == 0:
			return (res, self.true_monkey)
		else:
			return (res, self.false_monkey)
	
	def add_item(self, item: int) -> None:
		self.items.append(item)

def run(input_data: List[str], **kwargs) -> int:
	monkeys = []
	for i in range(0, len(input_data), 7):
		monkeys.append(Monkey(input_data[i+1:i+6]))
	
	mod_val = product(set([m.test for m in monkeys]))
	for _ in range(10000):
		for monkey in monkeys:
			while monkey.items:
				item, new_monkey = monkey.handle_item(mod_val)
				monkeys[new_monkey].add_item(item)
	
	monkey_counts = [m.total_inspected for m in monkeys]
	monkey_counts.sort(reverse=True)
	return monkey_counts[0] * monkey_counts[1]