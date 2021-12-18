from typing import List
from math import atan2, degrees, gcd
from utils.field.two_d import Cell, Field
import itertools as it


class Spot(Cell):
	def set_value(self, v: str) -> None:
		self.value = v == "#"

	def set_viewable_asteroids(self, count: int) -> None:
		self.viewable_asteroids = count

	def get_angle(self, origin: "Spot") -> float:
		offset = 270 if self.y < origin.y or self.x > origin.x else -90
		return degrees(atan2(origin.x-self.x, origin.y-self.y)) + offset


class AsteroidBelt(Field):
	def count_asteroids_viewable(self, spot: Spot) -> int:
		def is_asteroid_viewable(asteroid: Spot) -> bool:
			if not asteroid.value:
				return False
			if asteroid == spot:
				return False
			x_difference = asteroid.x - spot.x
			y_difference = asteroid.y - spot.y
			com_denom = gcd(x_difference, y_difference)
			if com_denom == 0:
				import pdb; pdb.set_trace()
			if com_denom == 1:
				return True
			x_interval = int(x_difference/com_denom)
			y_interval = int(y_difference/com_denom)

			def gen_coords(start, end, interval) -> List[int]:
				if interval == 0:
					return []
				start += interval
				return range(start, end, interval)

			for x, y in it.zip_longest(
				gen_coords(spot.x, asteroid.x, x_interval),
				gen_coords(spot.y, asteroid.y, y_interval),
			):
				if not x: x = spot.x
				if not y: y = spot.y
				if self.items[x][y].value:
					return False
			return True

		return self.apply(filterer=lambda x: is_asteroid_viewable(x))

	def set_asteroid_view_counts(self) -> None:
		self.apply(
			filterer=lambda x: x.value,
			transform=lambda x: x.set_viewable_asteroids(self.count_asteroids_viewable(x))
		)

	def print(self) -> None:
		for x in range(len(self.items)):
			for y in range(len(self.items[0])):
				print(self.items[x][y].value, end="")
			print()
		print()


def run(input_data: List[str]) -> int:
	asteroid_field = AsteroidBelt.create_from_input(input_data, Spot)
	asteroid_field.set_asteroid_view_counts()
	all_asteroids = asteroid_field.gen_cells(filterer=lambda x: x.value)
	all_asteroids = sorted(all_asteroids, key=lambda x: x.viewable_asteroids, reverse=True)
	ims = all_asteroids.pop(0)
	asteroids_by_angle = {}
	for a in all_asteroids:
		asteroids_by_angle.setdefault(a.get_angle(ims), []).append(a)

	for a_list in asteroids_by_angle.values():
		# manhattan distance is sufficient because all asteroids in a list
		# are at the same angle
		a_list.sort(key=lambda x: abs(x.x-ims.x) + abs(x.y-ims.y))

	i = 0
	all_angles = []
	for _ in range(200):
		if i >= len(all_angles):
			all_angles = sorted(asteroids_by_angle.keys())
			i = 0
		angle = all_angles[i]
		destroyed_asteroid = asteroids_by_angle[angle].pop(0)
		if not asteroids_by_angle[angle]: del asteroids_by_angle[angle]
		i += 1
	return destroyed_asteroid.y * 100 + destroyed_asteroid.x
