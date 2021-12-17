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


def print_cups(cup) -> None:
	c = cup
	cups_str = str(c.num) + " "
	while c.clockwise != cup:
		c = c.clockwise
		cups_str += str(c.num) + " "
	return cups_str

def move(cup, cups_dict, max_val) -> Cup:
	print(" -- move -- ")
	print(f"cups: {print_cups(cup)}")
	removed_cups = [cup.clockwise, cup.clockwise.clockwise, cup.clockwise.clockwise.clockwise]
	print(f"pick up: {removed_cups[0].num} {removed_cups[1].num} {removed_cups[2].num}")
	cup.add_clockwise(cup.clockwise.clockwise.clockwise.clockwise)
	for i in range(max_val):
		dest_cup = cup.num - (i + 1)
		if dest_cup < 1: dest_cup = max_val + dest_cup
		if dest_cup not in [c.num for c in removed_cups]:
			break
	else:
		raise Exception("couldn't find a cup")
	print(f"destination: {dest_cup}")
	destination_cup = cups_dict[dest_cup]
	while removed_cups: destination_cup.insert_clockwise(removed_cups.pop())
	print(f"cups: {print_cups(cup)}")
	print()
	return cup.clockwise



def run(input_data: List[str]) -> int:
	cups_data = input_data[0]
	cups_dict = {}
	first_cup = None
	prev_cup = None
	for i in range(len(cups_data)):
		new_cup_num = int(cups_data[i])
		new_cup = Cup(new_cup_num)
		cups_dict[new_cup_num] = new_cup
		if not prev_cup: first_cup = new_cup
		else: prev_cup.add_clockwise(new_cup)
		prev_cup = new_cup
	new_cup.add_clockwise(first_cup)

	current_cup = first_cup
	max_val = max(cups_dict.keys())
	for _ in range(100):
		current_cup = move(current_cup, cups_dict, max_val)

	final_value = 0
	start_cup = cups_dict[1]
	cup = start_cup
	while cup.clockwise != start_cup:
		cup = cup.clockwise
		final_value *= 10
		final_value += cup.num
	return final_value