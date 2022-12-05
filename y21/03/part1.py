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

	def get_gamma_val(self) -> str:
		if self.num_ones > self.num_zeros:
			return "1"
		return "0"

	def get_epsilon_val(self) -> str:
		if self.num_ones > self.num_zeros:
			return "0"
		return "1"

def run(input_data: List[str], **kwargs) -> int:
	counters = [Counter() for i in range(0, len(input_data[0].strip()))]
	for datum in input_data:
		datum = datum.strip()
		for i in range(0, len(datum)):
			counters[i].increment(datum[i])
	gamma = int(str.join("", [counter.get_gamma_val() for counter in counters]), base=2)
	epsilon = int(str.join("", [counter.get_epsilon_val() for counter in counters]), base=2)
	return gamma * epsilon
