from typing import List, Set

def run(input_data: List[str], **kwargs) -> int:
	total: int = 0
	letters_list: List[Set[str]] = []
	for datum in input_data:
		if not datum or datum == "\n":
			total += len(set.intersection(*letters_list))
			letters_list = []
			continue
		letters_list.append(set(datum.strip()))
	total += len(set.intersection(*letters_list))
	return total