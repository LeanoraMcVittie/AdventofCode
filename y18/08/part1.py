from typing import List


def sum_metadata_in_node(node_data):
	num_nodes = node_data[0]
	num_metadata = node_data[1]
	idx = 2
	metadata_sum = 0
	for _ in range(num_nodes):
		sub_metadata, s_idx = sum_metadata_in_node(node_data[idx:])
		idx += s_idx
		metadata_sum += sub_metadata
	for md in node_data[idx:idx+num_metadata]:
		metadata_sum += md
	return metadata_sum, idx + num_metadata


def run(input_data: List[str], **kwargs) -> int:
	license_file = input_data[0].split(" ")
	metadata, end = sum_metadata_in_node([int(l) for l in license_file])
	assert end == len(license_file)
	return metadata