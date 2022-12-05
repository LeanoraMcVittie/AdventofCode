from typing import List

class Cup:
	def __init__(self, num) -> None:
		self.num = num
		self.clockwise = None

	def add_counterclockwise(self, ccup: "Cup") -> None:
		ccup.clockwise = self

	def add_clockwise(self, ccup: "Cup") -> None:
		self.clockwise = ccup

	def insert_clockwise(self, ccup: "Cup") -> None:
		ccup.clockwise = self.clockwise
		self.clockwise = ccup


def move(cup, cups_list, max_val) -> Cup:
	removed_cups = [cup.clockwise, cup.clockwise.clockwise, cup.clockwise.clockwise.clockwise]
	cup.add_clockwise(cup.clockwise.clockwise.clockwise.clockwise)
	for i in range(max_val):
		dest_cup = cup.num - (i + 1)
		if dest_cup < 1: dest_cup = max_val + dest_cup
		if dest_cup not in [c.num for c in removed_cups]:
			break
	else:
		raise Exception("couldn't find a cup")
	destination_cup = cups_list[dest_cup]
	while removed_cups: destination_cup.insert_clockwise(removed_cups.pop())
	return cup.clockwise


def run(input_data: List[str], **kwargs) -> int:
	cups_data = input_data[0]
	cups_list = [None for _ in range(10)]
	first_cup = None
	prev_cup = None
	for i in range(len(cups_data)):
		new_cup_num = int(cups_data[i])
		new_cup = Cup(new_cup_num)
		cups_list[new_cup_num] = new_cup
		if not prev_cup: first_cup = new_cup
		else: prev_cup.add_clockwise(new_cup)
		prev_cup = new_cup

	max_val = 9
	while max_val < 1000000:
		max_val += 1
		new_cup = Cup(max_val)
		cups_list.append(new_cup)
		prev_cup.add_clockwise(new_cup)
		prev_cup=new_cup
	new_cup.add_clockwise(first_cup)

	current_cup = first_cup
	for _ in range(10000000):
		current_cup = move(current_cup, cups_list, max_val)

	cup = cups_list[1]
	return cup.clockwise.num * cup.clockwise.clockwise.num