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

	def get_parent_orbits(self, all_satellites) -> List[str]:
		if self.center_name == "COM":
			return [self.name]
		return all_satellites[self.center_name].get_parent_orbits(all_satellites) + [self.name]

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

	def get_distance(self, start, end) -> int:
		orbit_map1 = self.satellites[start].get_parent_orbits(self.satellites)
		orbit_map2 = self.satellites[end].get_parent_orbits(self.satellites)
		between_bodies = set.symmetric_difference(set(orbit_map1), set(orbit_map2))
		return len(between_bodies) - 2



def run(input_data: List[str]) -> int:
	map = Map(input_data)
	return map.get_distance("YOU", "SAN")
