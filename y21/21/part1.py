from typing import List


WINNING_SCORE: int = 1000


class Die:
	def __init__(self) -> None:
		self.last_roll = 0
		self.num_rolls = 0

	def roll(self) -> int:
		self.last_roll += 1
		if self.last_roll > 100:
			self.last_roll = self.last_roll % 100
		self.num_rolls += 1
		return self.last_roll


class Player:
	def __init__(self, start_pos) -> None:
		self.position = start_pos
		self.score = 0

	def move(self, die: Die) -> int:
		moves = sum(die.roll() for _ in range(3))
		self.position = (self.position+moves) % 10
		if self.position == 0: self.position = 10
		self.score += self.position
		return self.score


class Game:
	def __init__(self, player1_position: int, player2_position: int) -> None:
		self.p1 = Player(player1_position)
		self.p2 = Player(player2_position)
		self.die = Die()

	def play(self) -> int:
		while True:
			if self.p1.move(self.die) >= WINNING_SCORE:
				print(self.p2.score)
				print(self.die.num_rolls)
				return self.p2.score * self.die.num_rolls
			if self.p2.move(self.die) >= WINNING_SCORE:
				print(self.p1.score)
				print(self.die.num_rolls)
				return self.p1.score * self.die.num_rolls

def run(input_data: List[str], **kwargs) -> int:
	_, p1 = input_data[0].split(": ")
	_, p2 = input_data[1].split(": ")
	game = Game(int(p1), int(p2))
	return game.play()
