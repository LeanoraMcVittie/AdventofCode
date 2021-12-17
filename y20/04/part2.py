from typing import Dict, List, Optional
from utils.utils import is_valid_hex

VALID_ECLS = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

class Passport:
	byr: Optional[str]
	iyr: Optional[str]
	eyr: Optional[str]
	hgt: Optional[str]
	hcl: Optional[str]
	ecl: Optional[str]
	pid: Optional[str]
	cid: Optional[str]

	def __init__(self, passport_data: List[str]) -> None:
		passport_field_data: List[str] = []
		for data in passport_data:
			passport_field_data.extend(data.split())
		passport_kv_pairs = [field.split(":") for field in passport_field_data]
		[setattr(self, k, v) for k, v in passport_kv_pairs]

	def validate(self) -> bool:
		return (
			self.check_byr() and 
			self.check_iyr() and 
			self.check_eyr() and 
			self.check_hgt() and 
			self.check_hcl() and 
			self.check_ecl() and 
			self.check_pid() and 
			self.check_cid()
		)

	def check_byr(self) -> bool:
		if not hasattr(self, "byr"):
			return False
		if len(self.byr) != 4:
			return False
		if int(self.byr) not in range(1920, 2003):
			return False
		return True

	def check_iyr(self) -> bool:
		if not hasattr(self, "iyr"):
			return False
		if len(self.iyr) != 4:
			return False
		if int(self.iyr) not in range(2010, 2021):
			return False
		return True

	def check_eyr(self) -> bool:
		if not hasattr(self, "eyr"):
			return False
		if len(self.eyr) != 4:
			return False
		if int(self.eyr) not in range(2020, 2031):
			return False
		return True

	def check_hgt(self) -> bool:
		if not hasattr(self, "hgt"):
			return False
		height_str = self.hgt[:-2]
		try:
			height = int(height_str, base=10)
		except ValueError:
			return False
		units = self.hgt[-2:]
		if units == "in" and height in range(59, 77):
			return True
		elif units == "cm" and height in range(150, 194):
			return True
		return False

	def check_hcl(self) -> bool:
		if not hasattr(self, "hcl"):
			return False
		if self.hcl[0] != "#":
			return False
		if len(self.hcl) != 7:
			return False
		return is_valid_hex(self.hcl[1:])

	def check_ecl(self) -> bool:
		if not hasattr(self, "ecl"):
			return False
		return self.ecl in VALID_ECLS

	def check_pid(self) -> bool:
		if not hasattr(self, "pid"):
			return False
		if len(self.pid) != 9:
			return False
		try:
			int(self.pid, base=10)
		except ValueError:
			return False
		return True

	def check_cid(self) -> bool:
		return True


def run(input_data: List[str]) -> int:
	passport_data: List[str] = []
	passports: List[Passport] = []
	for datum in input_data:
		if datum == "\n":
			passports.append(Passport(passport_data))
			passport_data = []
			continue
		passport_data.append(datum)
	passports.append(Passport(passport_data))
	return sum([passport.validate() for passport in passports])
