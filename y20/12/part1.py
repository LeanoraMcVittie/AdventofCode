from typing import List
from functools import partial


class Instruction:
	code: str
	amt: int

	def __init__(self, datum: str) -> None:
		self.code = datum[0]
		self.amt = int(datum[1:])

class Ship:
	direction: str
	east: int
	north: int

	def __init__(self) -> None:
		self.direction = "E"
		self.east = 0
		self.north = 0

	def _move(self, direction: str, amount: int) -> None:
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


	def _turn(self, direction: str, amount: int) -> None:
		for i in range(0, int(amount/90)):
			self.direction = {
				"R" : {
					"E": "S",
					"S": "W",
					"W": "N",
					"N": "E",
				},
				"L" : {
					"E": "N",
					"N": "W",
					"W": "S",
					"S": "E",
				},
			}[direction][self.direction]

	def follow_instruction(self, instr: Instruction) -> None:
		{
			"F": partial(self._move, self.direction),
			"N": partial(self._move, instr.code),
			"S": partial(self._move, instr.code),
			"E": partial(self._move, instr.code),
			"W": partial(self._move, instr.code),
			"R": partial(self._turn, instr.code),
			"L": partial(self._turn, instr.code),
		}[instr.code](instr.amt)

	def manhattan_distance(self) -> int:
		return abs(self.east) + abs(self.north)

def run(input_data: List[str], **kwargs) -> int:
	ship = Ship()
	for datum in input_data:
		ship.follow_instruction(Instruction(datum))
	return ship.manhattan_distance()
