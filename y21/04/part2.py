from typing import List


class Board:
	elements: List[List[int]]
	unmarked: List[int]
	rows: List[int]
	cols: List[int]
	won: bool

	def __init__(self, board_data: List[str]) -> None:
		self.elements = [[int(num) for num in row.split(" ")] for row in board_data]
		self.unmarked = [elem for row in self.elements for elem in row]
		self.rows = [0 for i in range(0, 5)]
		self.cols = [0 for i in range(0, 5)]
		self.won = False

	def add_ball(self, ball: int) -> bool:
		if self.won:
			return False
		if ball not in self.unmarked:
			return False
		self.unmarked.remove(ball)
		for i in range(0, 5):
			for j in range(0, 5):
				if self.elements[i][j] == ball:
					self.rows[i] += 1
					self.cols[j] += 1
					if self.rows[i] == 5 or self.cols[j] == 5:
						self.won = True
					return self.won

	def score(self, winning_ball: int) -> int:
		return sum(self.unmarked) * winning_ball


def run(input_data: List[str]) -> int:
	balls: List[int] = [int(num) for num in input_data[0].split(",")]
	boards: List[Board] = []
	wins: int = 0
	for i in range(2, len(input_data), 6):
		boards.append(Board([input_data[j].replace("  ", " ") for j in range(i, i+5)]))
	for ball in balls:
		for board in boards:
			if board.add_ball(ball):
				wins += 1
			if wins == len(boards):
				return board.score(ball)