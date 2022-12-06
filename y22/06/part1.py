from typing import List

def run(input_data: List[str], **kwargs) -> int:
	d = input_data[0]
	for i in range(len(d)-4):
		if len(set(d[i:i+4])) == 4:
			return i + 4