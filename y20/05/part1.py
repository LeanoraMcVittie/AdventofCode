from typing import List

def run(input_data: List[str]) -> int:
	max_id: int = 0
	for boarding_pass in input_data:
		row: int = int(boarding_pass[:7].replace("F", "0").replace("B", "1"), base=2)
		seat: int = int(boarding_pass[7:].replace("L", "0").replace("R", "1"), base=2)
		seat_id = (row * 8) + seat
		max_id = max(max_id, seat_id)
	return max_id