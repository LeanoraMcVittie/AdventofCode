from typing import List

def run(input_data: List[str]) -> int:
	cal_counts = []
	sum = 0
	for snack in input_data:
		if snack == "":
			cal_counts.append(sum)
			sum = 0
		else:
			sum += int(snack)
	cal_counts.append(sum)
	cal_counts.sort(reverse=True)
	return cal_counts[0] + cal_counts[1] + cal_counts[2]

