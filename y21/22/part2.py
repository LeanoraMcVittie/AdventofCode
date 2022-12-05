from typing import List
from dataclasses import dataclass
import itertools as it


@dataclass
class Region:
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

	def split_if_overlap(self, r: "Region") -> List["Region"]:
		if (
			r.maxx < self.minx
			or r.maxy < self.miny
			or r.maxz < self.minz
			or r.minx > self.maxx
			or r.miny > self.maxy
			or r.minz > self.maxz
		): return [self]

		new_regions = []
		if r.maxx >= self.minx and self.maxx > r.maxx:
			new_regions.append(
				Region(
					minx=r.maxx + 1,
					maxx=self.maxx,
					miny=self.miny,
					maxy=self.maxy,
					minz=self.minz,
					maxz=self.maxz,
				)
			)
			self.maxx = r.maxx
		if r.minx <= self.maxx and self.minx < r.minx:
			new_regions.append(
				Region(
					minx=self.minx,
					maxx=r.minx - 1,
					miny=self.miny,
					maxy=self.maxy,
					minz=self.minz,
					maxz=self.maxz,
				)
			)
			self.minx = r.minx
		if r.maxy >= self.miny and self.maxy > r.maxy:
			new_regions.append(
				Region(
					minx=self.minx,
					maxx=self.maxx,
					miny=r.maxy + 1,
					maxy=self.maxy,
					minz=self.minz,
					maxz=self.maxz,
				)
			)
			self.maxy = r.maxy
		if r.miny <= self.maxy and self.miny < r.miny:
			new_regions.append(
				Region(
					minx=self.minx,
					maxx=self.maxx,
					miny=self.miny,
					maxy=r.miny - 1,
					minz=self.minz,
					maxz=self.maxz,
				)
			)
			self.miny = r.miny
		if r.maxz >= self.minz and self.maxz > r.maxz:
			new_regions.append(
				Region(
					minx=self.minx,
					maxx=self.maxx,
					miny=self.miny,
					maxy=self.maxy,
					minz=r.maxz + 1,
					maxz=self.maxz,
				)
			)
			self.maxz = r.maxz
		if r.minz <= self.maxz and self.minz < r.minz:
			new_regions.append(
				Region(
					minx=self.minx,
					maxx=self.maxx,
					miny=self.miny,
					maxy=self.maxy,
					minz=self.minz,
					maxz=r.minz - 1,
				)
			)
			self.minz = r.minz
		return new_regions

	def total(self) -> int:
		return (1+self.maxx-self.minx) * (1+self.maxy-self.miny) * (1+self.maxz-self.minz)

def run(input_data: List[str], **kwargs) -> int:
	on_regions = []
	for datum in input_data:
		setting, coords_str = datum.split(" ")
		setting = setting == "on"
		r = Region.parse(coords_str)
		new_on_regions = []
		for o in on_regions: new_on_regions.extend(o.split_if_overlap(r))
		if setting: new_on_regions.append(r)
		on_regions = new_on_regions

	return sum(r.total() for r in on_regions)
