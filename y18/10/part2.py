from typing import List
from utils.field.two_d import Cell, Coord, Field
import re


def move(
	positions: List[Coord], 
	velocities: List[Coord], 
	interval: int
) -> List[Coord]:
	new_pos = []
	for i in range(len(positions)):
		new_pos.append(
			Coord(
				positions[i].x + (velocities[i].x * interval),
				positions[i].y + (velocities[i].y * interval)
			)
		)
	return new_pos


def run(input_data: List[str], **kwargs) -> int:
	positions = []
	velocities = []
	for datum in input_data:
		matches = re.findall("<( *-?[0-9]+,\ *-?[0-9]+)>", datum)
		posx, posy = matches[0].split(", ")
		pos = Coord(int(posx), int(posy))
		velx, vely = matches[1].split(", ")
		vel = Coord(int(velx), int(vely))
		positions.append(pos)
		velocities.append(vel)

	count = 0
	if not kwargs["is_test"]:
		for mult in [10000, 330, 10, 2]:
			positions = move(positions, velocities, mult)
			count += mult

		new_positions = []	
		for pos in positions:
			new_pos = Coord(pos.x - 150, pos.y - 100)
			new_positions.append(new_pos)
		positions = new_positions

	done = input()
	while not done:
		field = Field(50, 100, Cell)
		field.apply(
			transform=lambda c: (
				c.set_value("#") if Coord(c.y, c.x) in positions else c.set_value(" ")
			)
		)
		field.print()
		done = input()
		count += 1
		positions = move(positions, velocities, 1)
	return count - 1

