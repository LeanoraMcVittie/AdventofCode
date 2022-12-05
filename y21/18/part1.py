from typing import List, Optional, Union
from math import ceil, floor


def is_int(to_test) -> bool:
	return isinstance(to_test, int)


class Exploded(Exception):
	def __init__(self, left: Optional[int], right: Optional[int]) -> None:
		assert left is None or isinstance(left, int)
		assert right is None or isinstance(right, int)
		self.left = left
		self.right = right


class Split(Exception):
	pass


class SnailfishNum:
	def __init__(
		self,
		left: Union[int, "SnailfishNum"],
		right: Union[int, "SnailfishNum"],
		nested_depth: int
	) -> None:
		self.left = left
		self.right = right
		self.nested_depth = nested_depth
		if not is_int(self.left):
			self.left.nest()
		if not is_int(self.right):
			self.right.nest()

	@classmethod
	def create_from_string(cls, snailfish_str: str) -> "SnailfishNum":
		assert snailfish_str[0] == "["
		assert snailfish_str[-1] == "]"
		if snailfish_str[1] == "[":
			index = 2
			unclosed_cnt = 1
			while unclosed_cnt > 0:
				if snailfish_str[index] == "[":
					unclosed_cnt += 1
				elif snailfish_str[index] == "]":
					unclosed_cnt -= 1
				index += 1
			left = cls.create_from_string(snailfish_str[1:index])
			right_snailfish_str = snailfish_str[index+1:-1]
		else:
			left = int(snailfish_str[1:snailfish_str.index(",")])
			right_snailfish_str = snailfish_str[snailfish_str.index(",")+1:-1]

		if right_snailfish_str[0] == "[":
			right = cls.create_from_string(right_snailfish_str)
		else:
			right = int(right_snailfish_str)
		snailfish_num = cls(left, right, 0)
		return snailfish_num


	def __str__(self) -> None:
		left = self.left if is_int(self.left) else self.left.__str__()
		right = self.right if is_int(self.right) else self.right.__str__()
		return f"[{left},{right}]"

	def add_left(self, explosion_piece):
		if is_int(self.left):
			self.left += explosion_piece
		else:
			self.left.add_left(explosion_piece)

	def add_right(self, explosion_piece):
		if is_int(self.right):
			self.right += explosion_piece
		else:
			self.right.add_right(explosion_piece)

	def nest(self) -> None:
		self.nested_depth += 1
		if not is_int(self.left): self.left.nest()
		if not is_int(self.right): self.right.nest()

	def magnitude(self) -> int:
		left = self.left if is_int(self.left) else self.left.magnitude()
		right = self.right if is_int(self.right) else self.right.magnitude()
		return 3*left + 2*right

	def _split(self, tobreak: int) -> "SnailfishNum":
		return SnailfishNum(
			left=floor(tobreak/2),
			right=ceil(tobreak/2),
			nested_depth=self.nested_depth+1,
		)

	def split(self) -> None:
		if is_int(self.left) and self.left > 9:
			self.left = self._split(self.left)
			raise Split()
		if not is_int(self.left):
			self.left.split()
		if is_int(self.right) and self.right > 9:
			self.right = self._split(self.right)
			raise Split()
		if not is_int(self.right):
			self.right.split()

	# There is a 0% chance I would have come up with this monstrosity
	# if I hadn't taken Professor Peter Buhr's concurrency course. So
	# thanks Professor Buhr...or maybe not. Up for debate really
	def explode(self) -> None:
		if self.nested_depth == 4:
			raise Exploded(self.left, self.right)

		assert self.nested_depth < 4

		while True:
			try:
				if not is_int(self.left):
					self.left.explode()
			except Exploded as explosion:
				if (
					explosion.right is not None
					and explosion.left is not None
				):
					self.left = 0
				if explosion.right is not None:
					if is_int(self.right):
						self.right += explosion.right
					else:
						self.right.add_left(explosion.right)
				if explosion.left is not None:
					raise Exploded(explosion.left, None)
			else:
				break

		while True:
			try:
				if not is_int(self.right):
					self.right.explode()
			except Exploded as explosion:
				if (
					explosion.left is not None
					and explosion.right is not None
				):
					self.right = 0
				if explosion.left is not None:
					if is_int(self.left):
						self.left += explosion.left
					else:
						self.left.add_right(explosion.left)
				if explosion.right is not None:
					raise Exploded(None, explosion.right)
			else:
				break

	def reduce(self) -> None:
		while True:
			while True:
				try: self.explode()
				except Exploded: pass
				else: break
			try: self.split()
			except Split: pass
			else: break

		print(f"{self}")


def run(input_data: List[str], **kwargs) -> int:
	print(input_data[0])
	snailfish_number = SnailfishNum.create_from_string(input_data.pop(0))
	for next_num in input_data:
		snailfish_number = SnailfishNum(
			snailfish_number,
			SnailfishNum.create_from_string(next_num),
			0
		)
		snailfish_number.reduce()
	return snailfish_number.magnitude()
