from typing import List

class Marble:
	def __init__(self, value: int):
		self.clockwise = None
		self.counterclockwise = None
		self.value = value
	
	def insert_clockwise(self, new) -> None:
		new.clockwise = self.clockwise
		new.counterclockwise = self
		self.clockwise.counterclockwise = new
		self.clockwise = new

	def remove_self(self) -> int:
		self.clockwise.counterclockwise = self.counterclockwise
		self.counterclockwise.clockwise = self.clockwise
		return self.value
		

def run(input_data: List[str], **kwargs) -> int:
	tokens = input_data[0].split(" ")
	num_players = int(tokens[0])
	num_marbles = int(tokens[-2]) + 1
	current = Marble(0)
	current.clockwise = current
	current.counterclockwise = current
	scores = [0] * num_players
	for i in range(1, num_marbles):
		if i % 23 == 0:
			scores[i % num_players] += i
			for _ in range(6): current = current.counterclockwise
			scores[i % num_players] += current.counterclockwise.remove_self()
		else:
			new = Marble(i)
			current.clockwise.insert_clockwise(new)
			current = new
	return max(scores)


