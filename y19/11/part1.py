from typing import Dict, List, Tuple
from y19.intcode import Halted, IntCode, WaitingOnInput


class Robot:
	def __init__(self, memory) -> None:
		self.x = 0
		self.y = 0
		self.direction = "U"
		self.computer = IntCode(memory)
		self.panels: Dict[Tuple[int, int], int] = {(0,0): 1}

	def turn(self, direction) -> None:
		self.direction = {
			("U", 1) : "R",
			("R", 1) : "D",
			("D", 1) : "L",
			("L", 1) : "U",
			("U", 0) : "L",
			("L", 0) : "D",
			("D", 0) : "R",
			("R", 0) : "U",
		}[(self.direction, direction)]

	def move(self) -> None:
		if self.direction == "U":
			self.y += 1
		elif self.direction == "D":
			self.y -= 1
		elif self.direction == "L":
			self.x -= 1
		elif self.direction == "R":
			self.x += 1

	def paint(self, color: int) -> None:
		# white is 1, black is 0
		self.panels[(self.x, self.y)] = color

	def run(self) -> None:
		try:
			while True:
				self.computer.add_input(self.panels.setdefault((self.x, self.y), 0))
				try:
					self.computer.run()
				except WaitingOnInput:
					pass
				self.paint(self.computer.next_output())
				self.turn(self.computer.next_output())
				self.move()
		except Halted:
			pass


def run(input_data: List[str], **kwargs) -> int:
	robot = Robot(input_data[0])
	robot.run()
	return len(robot.panels)
