from typing import List
from y19.intcode import IntCode
from utils.field.two_d import Cell, Field


def binary_search(low: int, high: int, is_too_high: Callable[[int], bool]) -> int:
	while high - low > 1:
		midpoint = int((high-low)/2)+low
		if is_too_high(midpoint): high = midpoint
		else: low = midpoint
	return low


def check_in_tractor_beam(program: str, x: int, y: int) -> bool:
	tractor_beam = IntCode(program)
	tractor_beam.add_input(x)
	tractor_beam.add_input(y)
	tractor_beam.run()
	return tractor_beam.next_output() == 1


def find_top_edge_of_tractor_beam_for_x_value(program: str, x: int) -> int:


def run(input_data: List[str]) -> int:
	# x = 0
	# y = 0
	# while True:
	# 	x = int(input("x: "))
	# 	y = int(input("y: "))
	# 	if y == "stop" or x == "stop": break
	# 	print(get_tractor_beam(input_data[0], x, y))
	# return x * 10000 + y

	return binary_search(0, 1000000, lambda x: x > 928)
