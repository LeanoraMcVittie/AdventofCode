from typing import Any, Callable, Dict, List

def get_input(module: str, prefix: str = "") -> List[str]:
	prefix += "_" if prefix else ""
	with open(f"{module}/{prefix}input.txt", 'r') as input_file:
		values: List[str] = input_file.readlines()
	return [v.strip() for v in values]

def is_valid_hex(hex: str) -> bool:
	try:
		int(hex, base=16)
	except ValueError:
		return False
	return True

# Example usage: 2019 day 18
def cache(cache_dict: Dict[Any, Any], compute_cache_key: Callable) -> Callable:
	def wrap(func: Callable) -> Callable:
		def wrapped_func(*args, **kwargs) -> Any:
			cache_key = compute_cache_key(*args, **kwargs)
			cached_result = cache_dict.get(cache_key)
			if cached_result: return cached_result
			result = func(*args, **kwargs)
			cache_dict[cache_key] = result
			return result
		return wrapped_func
	return wrap
