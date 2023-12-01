from typing import List
import re

VALID_DIGITS_MAP = {
	"0": 0, 
	"1": 1,
	"2": 2,
	"3": 3, 
	"4": 4, 
	"5": 5, 
	"6": 6,
	"7": 7, 
	"8": 8,
	"9": 9, 
	"one": 1, 
	"two": 2,
	"three": 3,
	"four": 4,
	"five": 5,
	"six": 6,
	"seven": 7,
	"eight": 8,
	"nine": 9,
}

REGEX = f"(?=({'|'.join(VALID_DIGITS_MAP.keys())}))"

def run(input_data: List[str], **kwargs) -> int:
	total = 0
	for line in input_data:
		digits = re.findall(REGEX, line)
		total += int(VALID_DIGITS_MAP[digits[0]]) * 10
		total += int(VALID_DIGITS_MAP[digits[-1]])
	return total	
