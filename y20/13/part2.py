from typing import List


class Bus:
	num: int
	offset: int

	def __init__(self, number: int, offset: int) -> None:
		self.num = number
		self.offset = offset


# I cheated and used this solution
# https://www.reddit.com/r/adventofcode/comments/kc4njx/comment/gfo4b1z/
# This is not the kind of problem I enjoy solving
def run(input_data: List[str]) -> int:
	bus_data = input_data[1].split(",")
	busses: List[Bus] = [
		Bus(int(bus_data[i]), i) 
		for i in range(0, len(bus_data)) 
		if bus_data[i] != "x"
	]
	interval = busses[0].num
	timestamp = 0
	for bus in busses[1:]:
		while (timestamp + bus.offset) % bus.num != 0:
			timestamp += interval
		interval *= bus.num
	return timestamp
