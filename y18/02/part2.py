from typing import List

def check_two(id1: str, id2: str) -> str:
	different_pos = -1
	for l in range(len(id1)):
		if id1[l] == id2[l]: continue
		if different_pos != -1: return ""
		different_pos = l
	return id1[:different_pos] + id1[different_pos+1:]


def run(input_data: List[str], **kwargs) -> int:
	unchecked_ids = input_data[1:]
	for id in input_data:
		for	comp in unchecked_ids:
			res = check_two(id, comp)
			if res: return res
		unchecked_ids.pop(0)
	raise Exception("something went wrong")