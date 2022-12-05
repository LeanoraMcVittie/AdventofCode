from typing import List

class Counter:
	num_ones: int
	num_zeros: int 

	def __init__(self) -> None:
		self.num_zeros = 0
		self.num_ones = 0

	def increment(self, val: str) -> None:
		if val == "0":
			self.num_zeros += 1
		elif val == "1":
			self.num_ones += 1
		else:
			raise Exception("Huh?")

	def get_most_common_val(self) -> str:
		if self.num_ones >= self.num_zeros:
			return "1"
		return "0"

	def get_least_common_val(self) -> str:
		if self.num_ones >= self.num_zeros:
			return "0"
		return "1"

def find_rating_value(possible_values: List[str], most_common: bool) -> int:
	counter = Counter()
	for i in range(0, len(possible_values[0])):
		for val in possible_values:
			counter.increment(val[i])
		common_val = (
			counter.get_most_common_val() 
			if most_common 
			else counter.get_least_common_val()
		)
		new_possible_values = []
		for val in possible_values:
			if val[i] == common_val:
				new_possible_values.append(val)
		possible_values = new_possible_values
		counter = Counter()
		if len(possible_values) == 1:
			return int(possible_values[0], base=2)

def run(input_data: List[str], **kwargs) -> int:
	oxygen_generator_val: int = find_rating_value(
		[datum.strip() for datum in input_data],
		True,
	)
	co2_scrubber_val: int = find_rating_value(
		[datum.strip() for datum in input_data],
		False,
	)
	return oxygen_generator_val * co2_scrubber_val