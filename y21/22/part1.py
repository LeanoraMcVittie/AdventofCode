from typing import List
from dataclasses import dataclass
import itertools as it

@dataclass
class Cube:
	minx: int
	maxx: int
	miny: int
	maxy: int
	minz: int
	maxz: int

	@classmethod
	def parse(cls, coords_str: str) -> "Cube":
		x_deets, y_deets, z_deets = coords_str.split(",")
		minx, maxx = x_deets[2:].split("..")
		miny, maxy = y_deets[2:].split("..")
		minz, maxz = z_deets[2:].split("..")
		return cls(
			int(minx),
			int(maxx),
			int(miny),
			int(maxy),
			int(minz),
			int(maxz),
		)


def run(input_data: List[str]) -> int:
	cubes_on = set()
	for datum in input_data:
		setting, coords_str = datum.split(" ")
		setting = setting == "on"
		c = Cube.parse(coords_str)
		if (
			c.maxx < -50
			or c.maxy < -50
			or c.maxz < -50
			or c.minx > 50
			or c.miny > 50
			or c.minz > 50
		):
			continue
		for x, y, z in it.product(
			range(c.minx, c.maxx+1),
			range(c.miny, c.maxy+1),
			range(c.minz, c.maxz+1),
		):
			if setting:
				cubes_on.add((x,y,z))
			else:
				cubes_on.discard((x,y,z))
	return len(cubes_on)
