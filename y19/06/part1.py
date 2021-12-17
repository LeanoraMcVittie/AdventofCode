from typing import List


class Satellite:
	def __init__(self, name: str, center_name: str) -> None:
		self.name = name
		self.center_name = center_name
		self.num_orbits = None if center_name != "COM" else 1

	def get_num_orbits(self, all_satellites) -> int:
		if not self.num_orbits:
			self.num_orbits = all_satellites[self.center_name].get_num_orbits(all_satellites) + 1
		return self.num_orbits


class Map:
	def __init__(self, orbits_list: List[str]) -> None:
		self.satellites = {}
		for orbit in orbits_list:
			cent_name, sat_name = orbit.split(")")
			self.satellites[sat_name] = Satellite(sat_name, cent_name)

	def get_orbits_count(self) -> int:
		total = 0
		for satellite in self.satellites.values():
			total += satellite.get_num_orbits(self.satellites)
		return total


def run(input_data: List[str]) -> int:
	map = Map(input_data)
	return map.get_orbits_count()
