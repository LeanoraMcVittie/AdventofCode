from typing import List
import itertools as it

class Moon:
	def __init__(self, position_str: str) -> None:
		x, y, z = position_str[1:-1].split(", ")
		_, x = x.split("=")
		_, y = y.split("=")
		_, z = z.split("=")
		self.position = [int(x),int(y),int(z)]
		self.velocity = [0,0,0]
		self.gravity = [0,0,0]

	def apply_gravity(self, moon: "Moon") -> None:
		for i in range(3):
			if self.position[i] > moon.position[i]:
				self.velocity[i] -= 1
				moon.velocity[i] += 1
			elif self.position[i] < moon.position[i]:
				self.velocity[i] += 1
				moon.velocity[i] -= 1

	def apply_velocity(self) -> None:
		for i in range(3):
			self.position[i] += self.velocity[i]

	def print(self) -> None:
		print(f"pos: ({self.position[0]}, {self.position[1]}, {self.position[2]})    vel: ({self.velocity[0]}, {self.velocity[1]}, {self.velocity[2]})")

	def energy(self) -> int:
		return sum(abs(p) for p in self.position) * sum(abs(v) for v in self.velocity)


def run(input_data: List[str], **kwargs) -> int:
	moons = []
	for datum in input_data:
		moons.append(Moon(datum))
	for i in range(1000):
		for m1, m2 in it.combinations(moons, 2):
			m1.apply_gravity(m2)
		for m in moons:
			m.apply_velocity()
	return sum(m.energy() for m in moons)
