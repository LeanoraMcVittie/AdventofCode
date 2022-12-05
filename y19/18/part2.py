from typing import Dict, List, Set, Tuple
from itertools import combinations
from utils.field.two_d import Cell, Coord, Field
from utils.utils import cache

class Loc(Cell):
	def cost(self) -> int:
		return 1

	def can_traverse(self):
		return self.value != "#"


def compute_distances_between_keys(vault: Field, keys: List[Loc]) -> Dict[Tuple[str, str], Tuple[int, Set[str]]]:
	result_dict: Dict[Tuple[str, str], Tuple[int, Set[str]]] = {}
	for k1, k2 in combinations(keys, 2):
		dist, path = vault.dijkstra(k1, k2, include_diagonals=False, filterer=lambda x: x.can_traverse())
		if not path:
			continue
		keys_in_path = [l.value for l in path[1 : -1] if l.value.islower()]
		keys_required = [l.value.lower() for l in path if l.value.isupper()]
		result_dict[(k1.value, k2.value)] = (dist, set(keys_required + keys_in_path))
		result_dict[(k2.value, k1.value)] = (dist, set(keys_required + keys_in_path))
	return result_dict


# WARNING: this isn't cleared between testing and running the actual script
cached_shortest_paths: Dict[str, int] = {}


def compute_cache_key(positions: List[Loc], keys_to_find: List[Loc], **kwargs) -> str:
	return str.join('', [k.value for k in positions + keys_to_find])


@cache(cache_dict=cached_shortest_paths, compute_cache_key=compute_cache_key)
def shortest_find_all_remaining_keys(
	vault: Field,
	positions: List[Loc],
	keys_to_find: List[Loc],
	all_key_distances: Dict[Tuple[str, str], Tuple[int, Set[str]]]
) -> int:
	if not keys_to_find:
		return 0
	min_length: int = None
	for position in positions:
		for key in keys_to_find:
			distance, prerequisite_keys = all_key_distances.get((position.value, key.value), (None, None))
			if not distance or any(rk in [k.value for k in keys_to_find] for rk in prerequisite_keys):
				continue
			steps_to_end = shortest_find_all_remaining_keys(
				vault=vault,
				positions=[p for p in positions if p is not position] + [key],
				keys_to_find=[k for k in keys_to_find if k is not key],
				all_key_distances=all_key_distances
			) + distance
			if not min_length or min_length > steps_to_end:
				min_length = steps_to_end
	return min_length


def run(input_data: List[str], **kwargs) -> int:
	vault = Field.create_from_input(input_data, Loc)
	key_locs = [l for l in vault.gen_cells(filterer=lambda x: x.value.islower())]
	# I fudged the inputs a bit to have distinct characters instead of starting with all @s
	starts = [l for l in vault.gen_cells(filterer=lambda x: x.value in ["@", "$", "&", "%"])]
	all_key_distances = compute_distances_between_keys(vault, key_locs + starts)
	result = shortest_find_all_remaining_keys(
		vault=vault,
		positions=starts,
		keys_to_find=key_locs,
		all_key_distances=all_key_distances,
	)
	return result
