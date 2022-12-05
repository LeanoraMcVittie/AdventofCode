from typing import List

ALL_FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"}

def check_passport(passport_data: List[str]) -> int:
	field_data: List[str] = []
	for data in passport_data:
		field_data.extend(data.split())
	fields = {field.split(":")[0] for field in field_data}
	missing_fields = ALL_FIELDS ^ fields
	if not missing_fields or missing_fields == {"cid"}:
		return 1
	return 0
	

def run(input_data: List[str], **kwargs) -> int:
	passport: List[str] = []
	valid_passports: int = 0
	for datum in input_data:
		if datum == "\n":
			valid_passports += check_passport(passport)
			passport = []
			continue
		passport.append(datum)
	valid_passports += check_passport(passport)
	return valid_passports