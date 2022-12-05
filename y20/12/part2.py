from typing import List
from functools import partial


class Instruction:
	code: str
	amt: int

	def __init__(self, datum: str) -> None:
		self.code = datum[0]
		self.amt = int(datum[1:])

class Waypoint:
	east: int
	north: int

	def __init__(self) -> None:
		self.east = 10
		self.north = 1

	def move(self, direction: str, amount: int) -> None:
		try:
			self.east = {
				"E": lambda x: self.east + x, 
				"W": lambda x: self.east - x,
			}[direction](amount) 
		except KeyError:
			self.north = {
				"N": lambda x: self.north + x,
				"S": lambda x: self.north - x, 
			}[direction](amount)


	def turn(self, rotation: str, amount: int) -> None:
		for i in range(0, int(amount/90)):
			tmp = {
				"R": -self.east, 
				"L" : self.east,
			}[rotation]
			self.east = {
				"R": self.north,
				"L": -self.north,
			}[rotation]
			self.north = tmp

class Ship:
	east: int
	north: int
	waypoint: Waypoint

	def __init__(self) -> None:
		self.east = 0
		self.north = 0
		self.waypoint = Waypoint()

	def _move(self, amount: int) -> None:
		self.east += self.waypoint.east * amount
		self.north += self.waypoint.north * amount

	def follow_instruction(self, instr: Instruction) -> None:
		{
			"F": self._move,
			"N": partial(self.waypoint.move, instr.code),
			"S": partial(self.waypoint.move, instr.code),
			"E": partial(self.waypoint.move, instr.code),
			"W": partial(self.waypoint.move, instr.code),
			"R": partial(self.waypoint.turn, instr.code),
			"L": partial(self.waypoint.turn, instr.code),
		}[instr.code](instr.amt)

	def manhattan_distance(self) -> int:
		return abs(self.east) + abs(self.north)

def run(input_data: List[str], **kwargs) -> int:
	ship = Ship()
	for datum in input_data:
		ship.follow_instruction(Instruction(datum))
	return ship.manhattan_distance()
