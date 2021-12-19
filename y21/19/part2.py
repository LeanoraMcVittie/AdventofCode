from typing import Dict, List, Set, Tuple
import itertools as it
from dataclasses import dataclass
from utils.math import THREE_DIMENSIONAL_ROTATION_MATRICIES
from collections import Counter

# I really really really HATE programmatic representations of 3D spaces
# I did not take Graphics for A Reason
# I also did not take advanced linear algebra, and I am missing that right now
# I barely even remember basic linear algebra
# I think I'm going to go to bed now. I'm getting loopy


@dataclass(frozen=True)
class Coordinate:
	x: int
	y: int
	z: int

	def rotate(self, rotation: int) -> Tuple[int, int, int]:
		m = THREE_DIMENSIONAL_ROTATION_MATRICIES[rotation]
		rotated_x = (self.x*m[0][0]) + (self.y*m[1][0]) + (self.z*m[2][0])
		rotated_y = (self.x*m[0][1]) + (self.y*m[1][1]) + (self.z*m[2][1])
		rotated_z = (self.x*m[0][2]) + (self.y*m[1][2]) + (self.z*m[2][2])
		return Coordinate(x=rotated_x, y=rotated_y, z=rotated_z)


@dataclass(frozen=True)
class Transform:
	# this could probably all be done in one matrix but that is not the kind of
	# math I want to do on a Sunday morning
	rotation: int # index into THREE_DIMENSIONAL_ROTATION_MATRICIES
	x_offset: int
	y_offset: int
	z_offset: int

	@classmethod
	def find_all_possible_transforms(
		cls,
		coord1: Coordinate,
		coord2: Coordinate,
	) -> List["Transform"]:
		possible_transforms = []
		for m_index in range(24): # iterate through THREE_DIMENSIONAL_ROTATION_MATRICIES
			rotated2 = coord2.rotate(m_index)
			transform = cls(
				rotation=m_index,
				x_offset=coord1.x - rotated2.x,
				y_offset=coord1.y - rotated2.y,
				z_offset=coord1.z - rotated2.z,
			)
			assert coord1 == transform.apply(coord2)
			possible_transforms.append(transform)
		return possible_transforms


	def apply(self, coord: Coordinate) -> Tuple[int, int, int]:
		transformed = coord.rotate(self.rotation)
		return Coordinate(
			x=transformed.x + self.x_offset,
			y=transformed.y + self.y_offset,
			z=transformed.z + self.z_offset,
		)


class Scanner:
	def __init__(self, num) -> None:
		self.num = num
		self.coords: List[Coordinate] = []
		self.relative_distances: Dict[Tuple[int, int, int], Tuple[Coordinate, Coordinate]] = {}
		self.transforms_to_s0 = []

	def add_coordinates(self, coord: Tuple[int, int, int]) -> None:
		self.coords.append(Coordinate(coord[0], coord[1], coord[2]))

	def get_all_relative_distances(self) -> None:
		if not self.relative_distances:
			for a, b in it.combinations(self.coords, 2):
				self.relative_distances[(a.x-b.x, a.y-b.y, a.z-b.z)] = (a,b)

	def transform_coords(self) -> List[Coordinate]:
		coordinates = [c for c in self.coords]
		for transform in self.transforms_to_s0:
			coordinates = [transform.apply(c) for c in coordinates]
		return coordinates

	def get_scanner_position_relative_to_0(self) -> Coordinate:
		scanner_pos = Coordinate(0, 0, 0)
		for transform in self.transforms_to_s0:
			scanner_pos = transform.apply(scanner_pos)
		return scanner_pos

	# This worked perfectly the FIRST TIME I ran it. It was also the first time
	# running any of the functions/classes it relies on! I laughed out loud,
	# yelled, jumped up and down - absolutely giddy! it was a good time :)
	def get_transform_if_exists(
		self, scanner: "Scanner"
	) -> List[Tuple[Tuple[int, int, int], Tuple[int, int, int]]]:
		# returns a Transform that can convert coords from scanner into coords with
		# the same reference point as self
		coord_pairs: Set[Tuple[Coordinate, Coordinate]] = set()
		for dist1, dist2 in it.product(
			self.relative_distances.keys(),
			scanner.relative_distances.keys(),
		):
			if (
				Counter([abs(dist1[i]) for i in range(3)])
				== Counter([abs(dist2[i]) for i in range(3)])
			):
				self_pair = self.relative_distances.get(dist1)
				scan_pair = scanner.relative_distances.get(dist2)
				coord_pairs.add((self_pair[0], scan_pair[0]))
				coord_pairs.add((self_pair[1], scan_pair[1]))

		if len(coord_pairs) < 12:
			return None

		transforms_counts = {}
		for coord1, coord2 in coord_pairs:
			for transform in Transform.find_all_possible_transforms(coord1, coord2):
				transforms_counts.setdefault(transform, 0)
				transforms_counts[transform] += 1

		for transform, count in transforms_counts.items():
			# I do not know why this is 11 and not 12
			# It should be 12
			# But there are 4 scanners in my input that only have a max
			# of 11 sooo....
			if count >= 11:
				return transform
		return None


def run(input_data: List[str]) -> int:
	index = 0
	all_scanners = []
	while index < len(input_data):
		scanner = Scanner(int(input_data[index][12:-4]))
		index += 1
		while index < len(input_data) and input_data[index] != "":
			scanner.add_coordinates([int(c) for c in input_data[index].split(",")])
			index += 1
		index += 1
		all_scanners.append(scanner)
	for scanner in all_scanners: scanner.get_all_relative_distances()

	still_lost_scanners = all_scanners[1:]
	scanners_to_match = [all_scanners[0]]
	done_scanners = []
	while len(still_lost_scanners) > 0:
		match_scanner = scanners_to_match.pop()
		for lost_scanner in all_scanners:
			if lost_scanner not in still_lost_scanners:
				continue
			transform = match_scanner.get_transform_if_exists(lost_scanner)
			print(f"checked {match_scanner.num} against {lost_scanner.num}", end="")
			if not transform:
				print()
				continue
			print(" transform found!")
			lost_scanner.transforms_to_s0 = [transform]
			lost_scanner.transforms_to_s0.extend(match_scanner.transforms_to_s0)
			scanners_to_match.append(lost_scanner)
			still_lost_scanners.remove(lost_scanner)

	manhattan_distances = []
	for s1, s2 in it.combinations(all_scanners, 2):
		c1 = s1.get_scanner_position_relative_to_0()
		c2 = s2.get_scanner_position_relative_to_0()
		manhattan_distance = abs(c1.x-c2.x) + abs(c1.y-c2.y) + abs(c1.z-c2.z)
		manhattan_distances.append(manhattan_distance)
	return max(manhattan_distances)
