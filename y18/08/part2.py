from typing import List


def get_value_of_node(node_data):
	num_children = node_data[0]
	num_metadata = node_data[1]
	idx = 2
	child_vals = []
	for _ in range(num_children):
		sub_value, s_idx = get_value_of_node(node_data[idx:])
		idx += s_idx
		child_vals.append(sub_value)
	
	node_value = 0
	for md in node_data[idx:idx+num_metadata]:
		if num_children == 0:
			node_value += md
		elif md <= num_children:
			node_value += child_vals[md-1]
	return node_value, idx + num_metadata


def run(input_data: List[str], **kwargs) -> int:
	license_file = input_data[0].split(" ")
	node_value, end = get_value_of_node([int(l) for l in license_file])
	assert end == len(license_file)
	return node_value