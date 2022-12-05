from typing import List, Tuple


class Mask:
	masked_bits: List[Tuple[int, str]]

	def __init__(self, mask: str) -> None:
		self.masked_bits = []
		for i in range(0, len(mask)):
			if mask[i] == "X":
				continue
			self.masked_bits.append((i, mask[i]))

	def mask_int(self, num: int) -> int:
		binary_str = str(bin(num))[2:]
		binary_list = ["0"] * (36-len(binary_str))
		binary_list.extend(list(binary_str))
		for bit in self.masked_bits:
			binary_list[bit[0]] = bit[1]
		return int(str.join("", binary_list), base=2)


def run(input_data: List[str], **kwargs) -> int:
	memory = [0] * 100000
	mask: Mask = None
	for datum in input_data:
		instruction, value = datum.split(" = ")
		if instruction == "mask":
			mask = Mask(value)
		else:
			mem_loc = int(instruction[4:-1])
			try:
				memory[mem_loc] = mask.mask_int(int(value))
			except IndexError:
				import pdb; pdb.set_trace()
	return sum(memory)

	