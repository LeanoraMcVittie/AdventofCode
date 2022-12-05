from typing import List

def run(input_data: List[str], **kwargs) -> int:
	data = [int(datum) for datum in input_data]
	data.append(0)
	data.append(max(data) + 3)
	data.sort()
	jolt1_count: int = 0
	jolt3_count: int = 0
	for i in range(1, len(data)):
		difference = data[i] - data[i-1]
		if difference == 1:
			jolt1_count += 1
		elif difference == 2:
			pass
		elif difference == 3:
			jolt3_count += 1
		else:
			raise Exception(f"Difference of {difference} between {data[i]} and {data[i-1]}")
	return jolt1_count * jolt3_count
