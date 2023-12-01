from __future__ import annotations

from typing import Dict, List, Tuple
from utils.field.two_d import Cell, Field
from functools import total_ordering

WHITESPACE: bool = True

CART_CHARS: List[str] = [">", "<", "^", "v"]
TRACK_CHARS: List[str] = ["|", "-", "\\", "/", "+"]


class Collision(Exception):
	def __init__(self, *carts) -> None:
		self.carts = carts


class Cart:
	DIRECTIONS: List[str] = ["L", "S", "R"]
	INTERSECTIION_MAP: Dict[str, List[str]] = {
		">" : ["^", ">", "v"],
			# "L": "^"
			# "S": ">"
			# "R": "v"
		"<": ["v", "<", "^"],
			# "L": "v"
			# "S": ">"
			# "R": "^"
		"^": ["<", "^", ">"],
			# "L": "<"
			# "S": "^"
			# "R": ">"
		"v": [">", "v", "<"],
			# "L": ">"
			# "S": "v"
			# "R": "<"
	}
	CURVE_MAP: Dict[str, Dict[str, str]] = {
		"\\": {"v": ">", ">": "v", "<": "^", "^": "<"},
		"/": {"v": "<", "<": "v", "^": ">", ">": "^"}
	}

	def __init__(self, dir: str, track_segment: Track):
		self.direction = dir
		self.turns = 0
		self.track_segment = track_segment
	
	def move_to(self, track_segment: Track) -> None:
		self.track_segment = track_segment
		rail = track_segment.value
		if rail == TRACK_CHARS[-1]:
			self.direction = self.INTERSECTIION_MAP[self.direction][self.turns % 3]
			self.turns += 1
		elif rail in TRACK_CHARS[2:4]:
			self.direction = self.CURVE_MAP[rail][self.direction]
		

@total_ordering
class Track(Cell):
	MOVE_MAP: Dict[str, Tuple[int, int]] = {
		"v": (1, 0),
		"^": (-1, 0),
		">": (0, 1),
		"<": (0, -1)
	}

	def __le__(self, other) -> bool:
		return (self.x, self.y) <= (other.x, other.y)

	def __eq__(self, other) -> bool:
		return (self.x, self.y) == (other.x, other.y)
	
	def init_value(self):
		self.value = None
		self.cart = None

	def cart_fix(self):
		self.cart = Cart(self.value, self)
		self.value = TRACK_CHARS[1] if self.cart.direction in CART_CHARS[:2] else TRACK_CHARS[0]
	
	def accept_cart(self, cart: Cart) -> None:
		assert self.value in TRACK_CHARS
		if self.cart is not None:
			raise Collision(cart, self.cart)
		self.cart = cart
		self.cart.move_to(self)

	def move(self, field: Field) -> None:
		assert self.cart is not None
		x, y = self.MOVE_MAP[self.cart.direction]
		field.get(self.x + x, self.y + y).accept_cart(self.cart)
		self.cart = None

	
def print_with_carts(field: Field) -> None:
	def get_val(t: Track) -> str:
		if t.cart:
			return t.cart.direction
		return t.value

	for x in range(field.x_size):
		for y in range(field.y_size):
			print(get_val(field.get(x, y)), end="")
		print()
	print()


def run(input_data: List[str], **kwargs) -> int:
	input_data[0] = input_data[0][:-1]
	field = Field.create_from_input(input_data, Track)
	field.apply(filterer=lambda t: t.value in CART_CHARS, transform=lambda t: t.cart_fix())
	carts = [c for c in field.gen_cells(filterer=lambda t: t.cart is not None, transform=lambda t: t.cart)]
	
	while len(carts) > 1:
		# print_with_carts(field)
		# input()
		crashed_carts = []
		carts.sort(key=lambda c: c.track_segment)
		for cart in carts:
			try:
				if cart not in crashed_carts:
					cart.track_segment.move(field)
			except Collision as collision:
				crashed_carts.extend(collision.carts)
				for c in collision.carts:
					c.track_segment.cart = None
		for cart in crashed_carts:
			carts.remove(cart)
	
	final = carts[0].track_segment
	return f"{final.y},{final.x}"
				

