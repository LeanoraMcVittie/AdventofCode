from typing import List

def run(input_data: List[str], **kwargs) -> int:
	all_ids: List[int] = [i for i in range(0, 859)]
	for boarding_pass in input_data:
		row: int = int(boarding_pass[:7].replace("F", "0").replace("B", "1"), base=2)
		seat: int = int(boarding_pass[7:].replace("L", "0").replace("R", "1"), base=2)
		seat_id = (row * 8) + seat
		all_ids.remove(seat_id)
	for seat_id in all_ids:
		if seat_id - 1 not in all_ids and seat_id + 1 not in all_ids:
			return seat_id
	raise Exception("well this sucks")