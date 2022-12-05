from typing import List

def digit_pair(istr: str, i: int) -> bool:
	if istr[i] != istr[i+1]:
		return False
	if i > 0 and istr[i-1] == istr[i]:
		return False
	if i+2 < len(istr) and istr[i+2] == istr[i]:
		return False
	return True

def run(input_data: List[str], **kwargs) -> int:
	start, end = input_data[0].split("-")
	start = int(start)
	end = int(end) + 1
	count = 0
	for i in range(start,end):
		istr = str(i)
		if any([
			int(istr[0]) > int(istr[1]),
			int(istr[1]) > int(istr[2]),
			int(istr[2]) > int(istr[3]),
			int(istr[3]) > int(istr[4]),
			int(istr[4]) > int(istr[5]),
		]):
			continue
		if any(digit_pair(istr, i) for i in range(5)):
			count += 1
	return count
