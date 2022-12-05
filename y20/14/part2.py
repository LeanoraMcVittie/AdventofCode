from typing import Generator, List, Tuple


class Mask:
	masked_bits: List[int]
	floating_bits: List[int]

	def __init__(self, mask: str) -> None:
		self.masked_bits = []
		self.floating_bits = []
		for i in range(0, len(mask)):
			if mask[i] == "X":
				self.floating_bits.append(i)
			elif mask[i] == "1":
				self.masked_bits.append(i)

	def gen_masked_ints(self, num: int) -> Generator[int, None, None]:
		binary_str = str(bin(num))[2:]
		binary_list = ["0"] * (36-len(binary_str))
		binary_list.extend(list(binary_str))
		for bit in self.masked_bits:
			binary_list[bit] = "1"
		num_floaters = len(self.floating_bits)
		floater_len = len(str(bin((2**num_floaters)-1)))-2
		for i in range(0, 2**num_floaters):
			binary_mask_values = str(bin(i))[2:]
			binary_mask_values = ("0" * (floater_len - len(binary_mask_values))) + binary_mask_values
			for j in range(0, num_floaters):
				binary_list[self.floating_bits[j]] = binary_mask_values[j]
			binary_str = str.join("", binary_list)
			yield int(binary_str, base=2)


def run(input_data: List[str], **kwargs) -> int:
	memory: Dict[int, int] = {}
	mask: Mask = None
	for datum in input_data:
		instruction, value = datum.split(" = ")
		if instruction == "mask":
			mask = Mask(value)
		else:
			for mem_loc in mask.gen_masked_ints(int(instruction[4:-1])):
				memory[mem_loc] = int(value)
	return sum(memory.values())

	