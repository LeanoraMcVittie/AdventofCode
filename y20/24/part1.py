from typing import List, Tuple


def tile_coordinates(directions: str) -> Tuple[int, int]:
	i = 0
	x = 0
	y = 0
	while i < len(directions):
		if directions[i] == "w": x -= 2
		elif directions[i] == "e": x += 2
		elif directions[i] == "n":
			y += 1
			i += 1
			if directions[i] == "w": x -= 1
			elif directions[i] == "e": x += 1
			else: raise Exception("w or e must follow n")
		elif directions[i] == "s":
			y -= 1
			i += 1
			if directions[i] == "w": x -= 1
			elif directions[i] == "e": x += 1
			else: raise Exception("w or e must follow s")
		else: raise Exception("w, e, n, and s are the only options")
		i += 1
	return x, y


def run(input_data: List[str]) -> int:
	black_tiles: List[Tuple[int, int]] = []

	for tile in input_data:
		coords = tile_coordinates(tile)
		if coords in black_tiles:
			black_tiles.remove(coords)
		else: black_tiles.append(coords)

	return len(black_tiles)