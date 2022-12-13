from typing import Any, Callable, Dict, List


def get_input(
    module: str, prefix: str = "", keep_whitespace: bool = False
) -> List[str]:
    prefix += "_" if prefix else ""
    with open(f"{module}/{prefix}input.txt", "r") as input_file:
        values: List[str] = input_file.readlines()
    if keep_whitespace:
        return values
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
            if cached_result:
                return cached_result
            result = func(*args, **kwargs)
            cache_dict[cache_key] = result
            return result

        return wrapped_func

    return wrap


def binary_search(low: int, high: int, is_too_high: Callable[[int], bool]) -> int:
    while high - low > 1:
        midpoint = int((high - low) / 2) + low
        if is_too_high(midpoint):
            high = midpoint
        else:
            low = midpoint
    return low

# is_lower: return True if the first parameter should be before the second parameter 
def merge_sort(data: List, is_lower: Callable[[Any, Any], bool]) -> List:
    if len(data) == 1:
        return data
    data1 = merge_sort(data[:len(data)//2], is_lower)
    data2 = merge_sort(data[len(data)//2:], is_lower)
    sorted_list = []
    for _ in range(len(data)):
        if not data2 or (data1 and is_lower(data1[0], data2[0])):
            sorted_list.append(data1.pop(0))
        else:
            sorted_list.append(data2.pop(0))
    return sorted_list


