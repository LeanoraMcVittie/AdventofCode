from typing import List

def run(input_data: List[str], **kwargs) -> int:
	time = int(input_data[0])
	busses = input_data[1].split(",")
	min_time = time * 2
	min_bus = 0
	for bus in busses:
		if bus == "x":
			continue
		bus = int(bus)
		wait_time = bus - (time % bus)
		print(f"bus {bus} has wait time {wait_time}")
		if time + wait_time < min_time:
			min_time = time + wait_time
			min_bus = bus
	return min_bus * (min_time - time)

