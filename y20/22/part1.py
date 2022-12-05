from typing import List

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
	i = 1
	while player_one and player_two:
		print(f" --- Round {i} --- ")
		p1 = player_one.pop(0)
		p2 = player_two.pop(0)
		if p1 > p2:
			print("Player 1 wins the round!")
			player_one.append(p1)
			player_one.append(p2)
		else:
			print("Player 2 wins the round!")
			player_two.append(p2)
			player_two.append(p1)
		i += 1
		print()

	winning_hand = player_one if player_one else player_two
	winning_hand.reverse()
	return sum((i+1)*winning_hand[i] for i in range(len(winning_hand)))
