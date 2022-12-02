from typing import List

MAP = {
	"X": "rock",
	"Y": "paper",
	"Z": "scissors",
	"A": "rock",
	"B": "paper",
	"C": "scissors",
}

SHAPE_SCORE = {
	"rock": 1,
	"paper": 2,
	"scissors": 3,
}

def run(input_data: List[str]) -> int:
	points = 0
	for d in input_data:
		opp, me = d.split(" ")
		opp = MAP[opp]
		me = MAP[me]
		points += SHAPE_SCORE[me]
		if opp == me:
			points += 3
		elif (
			(opp == "scissors" and me == "rock") or
			(opp == "paper" and me == "scissors") or 
			(opp == "rock" and me == "paper")
		):
			points += 6

	return points
