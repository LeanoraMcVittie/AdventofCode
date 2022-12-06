from typing import List

def run(input_data: List[str], **kwargs) -> int:
	d = input_data[0]
	for i in range(len(d)-14):
		if len(set(d[i:i+14])) == 14:
			return i + 14