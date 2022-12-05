from typing import Dict, List
from dataclasses import dataclass


@dataclass
class GameResult:
	winner: bool  # True is Player 1
	winning_hand: List[int]


class Game:
	round_results: Dict[str, GameResult] = {}
	game_counter = 1

	def __init__(self, player_one: List[int], player_two: List[int]) -> None:
		self.player_one = player_one
		self.player_two = player_two
		self.new_rounds: List[str] = []
		self.game_num = Game.game_counter
		Game.game_counter += 1

	def play(self) -> GameResult:
		print(f"===== Game {self.game_num} starting! =====")
		result = "uninitialized"
		# returns True if player 1 wins, False if player 2 wins
		try:
			while self.player_one and self.player_two:
				print(f" --- Round {len(self.new_rounds) + 1} of Game {self.game_num} --- ")
				print(f"Player 1's deck: {self.player_one}")
				print(f"Player 2's deck: {self.player_two}")
				round_state = str.join(
					",", 
					(
						str.join(" ", [str(c) for c in self.player_one]),
						str.join(" ", [str(c) for c in self.player_two]),
					),
				)
				if Game.round_results.get(round_state):
					print("This round has been played before in another game - returning that result")
					result = Game.round_results.get(round_state)
					return result
				if round_state in self.new_rounds:
					print("Repeated round - Player 1 wins this game")
					result = GameResult(winner=True, winning_hand=self.player_one)
					return result
				self.new_rounds.append(round_state)
				self.round()
			result = (
				GameResult(winner=True, winning_hand=self.player_one) 
				if self.player_one else GameResult(winner=False, winning_hand=self.player_two)
			)
			return result
		finally:
			print(f" ===== Game {self.game_num} completed ===== ")
			print()
			for r in self.new_rounds:
				Game.round_results[r] = result

	def round(self) -> None:
		def p1_wins(p1: int, p2: int) -> None:
			print("Player 1 wins the round!")
			self.player_one.append(p1)
			self.player_one.append(p2)

		def p2_wins(p1: int, p2: int) -> None:
			print("Player 2 wins the round!")
			self.player_two.append(p2)
			self.player_two.append(p1)
		
		p1 = self.player_one.pop(0)
		p2 = self.player_two.pop(0)
		print(f"Player 1 plays {p1}")
		print(f"Player 2 plays {p2}")
		if p1 > len(self.player_one) or p2 > len(self.player_two):
			if p1 > p2:
				p1_wins(p1, p2)
			else:
				p2_wins(p1, p2)
		elif Game(self.player_one[:p1], self.player_two[:p2]).play().winner:
			p1_wins(p1, p2)
		else:
			p2_wins(p1, p2)


def run(input_data: List[str], **kwargs) -> int:
	player_one = []
	player_two = []
	i = 1
	while input_data[i] != "":
		player_one.append(int(input_data[i]))
		i += 1
	i += 2
	while i < len(input_data):
		player_two.append(int(input_data[i]))
		i += 1

	winning_hand = Game(player_one, player_two).play().winning_hand
	print(winning_hand)
	winning_hand.reverse()
	return sum((i+1)*winning_hand[i] for i in range(len(winning_hand)))
