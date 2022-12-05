from typing import List
import itertools as it
from collections import Counter


WINNING_SCORE: int = 21
POSITION_AND_NUM_MOVES_TO_SCORE = {(1, 3): 4, (1, 4): 5, (1, 5): 6, (1, 6): 7, (1, 7): 8, (1, 8): 9, (1, 9): 10, (2, 3): 5, (2, 4): 6, (2, 5): 7, (2, 6): 8, (2, 7): 9, (2, 8): 10, (2, 9): 1, (3, 3): 6, (3, 4): 7, (3, 5): 8, (3, 6): 9, (3, 7): 10, (3, 8): 1, (3, 9): 2, (4, 3): 7, (4, 4): 8, (4, 5): 9, (4, 6): 10, (4, 7): 1, (4, 8): 2, (4, 9): 3, (5, 3): 8, (5, 4): 9, (5, 5): 10, (5, 6): 1, (5, 7): 2, (5, 8): 3, (5, 9): 4, (6, 3): 9, (6, 4): 10, (6, 5): 1, (6, 6): 2, (6, 7): 3, (6, 8): 4, (6, 9): 5, (7, 3): 10, (7, 4): 1, (7, 5): 2, (7, 6): 3, (7, 7): 4, (7, 8): 5, (7, 9): 6, (8, 3): 1, (8, 4): 2, (8, 5): 3, (8, 6): 4, (8, 7): 5, (8, 8): 6, (8, 9): 7, (9, 3): 2, (9, 4): 3, (9, 5): 4, (9, 6): 5, (9, 7): 6, (9, 8): 7, (9, 9): 8, (10, 3): 3, (10, 4): 4, (10, 5): 5, (10, 6): 6, (10, 7): 7, (10, 8): 8, (10, 9): 9}
MOVES_COUNTS = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}


class Player:
	def __init__(self, start_pos) -> None:
		self.position = start_pos
		self.round_to_num_wins = {}
		self.num_rounds = 0

	def play_all_games(self) -> int:
		pos_and_score_counts = {(self.position, 0): 1}
		while pos_and_score_counts:
			wins_this_round = 0
			self.num_rounds += 1
			new_pos_and_score_counts = {}
			for pos, score in pos_and_score_counts.keys():
				for moves, count in MOVES_COUNTS.items():
					new_pos = POSITION_AND_NUM_MOVES_TO_SCORE[(pos,moves)]
					new_score = score + new_pos
					num_games_in_state = pos_and_score_counts[(pos,score)] * count
					if new_score >= WINNING_SCORE:
						wins_this_round += num_games_in_state
					else:
						new_pos_and_score_counts.setdefault((new_pos,new_score), 0)
						new_pos_and_score_counts[(new_pos,new_score)] += num_games_in_state
			pos_and_score_counts = new_pos_and_score_counts
			self.round_to_num_wins[self.num_rounds] = wins_this_round


class Game:
	def __init__(self, player1_position: int, player2_position: int) -> None:
		self.p1 = Player(player1_position)
		self.p2 = Player(player2_position)

	def play(self) -> int:
		self.p1.play_all_games()
		self.p2.play_all_games()
		total_p1_wins = 0
		prod = 1
		for i in range(1, len(self.p1.round_to_num_wins)+1):
			total_p1_wins += self.p1.round_to_num_wins[i] * prod
			prod *= 27
			prod -= self.p2.round_to_num_wins[i]
		total_p2_wins = 0
		prod = 1
		for i in range(1, len(self.p2.round_to_num_wins)+1):
			prod *= 27
			prod -= self.p1.round_to_num_wins[i]
			total_p2_wins += self.p2.round_to_num_wins[i] * prod
		return max(total_p1_wins, total_p2_wins)


def run(input_data: List[str], **kwargs) -> int:
	_, p1 = input_data[0].split(": ")
	_, p2 = input_data[1].split(": ")
	game = Game(int(p1), int(p2))
	return game.play()
