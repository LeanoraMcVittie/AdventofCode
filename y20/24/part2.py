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

# 3672
# this still isn't snappy, it takes well over a second, but it's much better
# than the first version
def day(black_tiles: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
	neighbors = [(-2,0),(-1,-1),(1,-1),(2,0),(1,1),(-1,1)]
	neighbor_counts: Dict[Tuple[int, int], int] = {}
	for x,y in black_tiles:
		for i,j in neighbors:
			n = (x+i,y+j)
			neighbor_counts.setdefault(n, 0)
			neighbor_counts[n] += 1

	new_black_tiles = []
	for c, v in neighbor_counts.items():
		if v == 2:
			new_black_tiles.append(c)
		elif v == 1 and c in black_tiles:
			new_black_tiles.append(c)
	return new_black_tiles


# this works, but is slow, almost three minutes to run to day 100. 
# I wrote almost all of the new day() in the time
# it took for this to run
def day_slow(black_tiles: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
	def count_black_neighbors(x: int, y: int) -> int:
		neighbors = [(-2,0),(-1,-1),(1,-1),(2,0),(1,1),(-1,1)]
		total = 0
		for n in neighbors:
			if (x+n[0],y+n[1]) in black_tiles:
				total += 1
		return total

	min_x = min(c[0] for c in black_tiles) - 2
	max_x = max(c[0] for c in black_tiles) + 2
	min_y = min(c[1] for c in black_tiles) - 1
	max_y = max(c[1] for c in black_tiles) + 1

	new_black_tiles = []
	for y in range(min_y, max_y+1):
		offset = 1 if y % 2 != min_x % 2 else 0
		for x in range(min_x+offset, max_x+3, 2):
			num_black_neighbors = count_black_neighbors(x, y)
			if (x,y) in black_tiles:
				if num_black_neighbors == 1 or num_black_neighbors == 2:
					new_black_tiles.append((x,y))
			else:
				if num_black_neighbors == 2:
					new_black_tiles.append((x,y))
	return new_black_tiles


def run(input_data: List[str]) -> int:
	black_tiles: List[Tuple[int, int]] = []

	for tile in input_data:
		coords = tile_coordinates(tile)
		if coords in black_tiles:
			black_tiles.remove(coords)
		else: black_tiles.append(coords)

	print(f"Day 0: {len(black_tiles)}")

	for i in range(100):
		black_tiles = day_slow(black_tiles)
		print(f"Day {i+1}: {len(black_tiles)}")

	return len(black_tiles)