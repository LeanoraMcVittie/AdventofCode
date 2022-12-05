from typing import List

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
		if any([
			istr[0] == istr[1],
			istr[1] == istr[2],
			istr[2] == istr[3],
			istr[3] == istr[4],
			istr[4] == istr[5],
		]):
			count += 1
	return count
