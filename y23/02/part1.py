from typing import List

MAXIMUMS = {
	"red": 12,
	"green": 13,
	"blue": 14,
}


def run(input_data: List[str], **kwargs) -> int:
	count = 0
	for line in input_data:
		game, rounds = line.split(": ")
		for round in rounds.split("; "):
			totals = {"red": 0, "green": 0, "blue": 0}
			for c in round.split(", "):
				amt, color = c.split()
				totals[color] += int(amt)
			if any(MAXIMUMS[k] < v for k, v in totals.items()): break
		else:
			_, game_id = game.split()
			count += int(game_id)
	return count
			