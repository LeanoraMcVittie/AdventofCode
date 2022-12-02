from typing import List

MAP = {
	"X": "lose",
	"Y": "tie",
	"Z": "win",
	"A": "rock",
	"B": "paper",
	"C": "scissors",
}

SHAPE_SCORE = {
	"rock": 1,
	"paper": 2,
	"scissors": 3,
}

LOSE_MAP = {
	"rock": "scissors",
	"scissors": "paper",
	"paper": "rock",
}

WIN_MAP = {
	"rock": "paper",
	"scissors": "rock",
	"paper": "scissors",
}

RES_SCORE = {
	"lose": 0,
	"tie": 3,
	"win": 6,
}

def run(input_data: List[str]) -> int:
	points = 0
	for d in input_data:
		opp, res = d.split(" ")
		opp = MAP[opp]
		res = MAP[res]
		points += RES_SCORE[res]
		if res == "tie":
			points += SHAPE_SCORE[opp]
		elif res == "lose":
			points += SHAPE_SCORE[LOSE_MAP[opp]]
		else:
			points += SHAPE_SCORE[WIN_MAP[opp]]

	return points
