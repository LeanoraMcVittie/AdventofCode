from typing import List
from y19.intcode import IntCode, OutputClear
from utils.field.two_d import Cell, Field


def run(input_data: List[str], **kwargs) -> int:
	vaccuum_robot = IntCode(input_data[0])
	vaccuum_robot.run()
	scaffolding_input = []
	current_row = ""
	while True:
		try: c = vaccuum_robot.next_output()
		except OutputClear: break
		if c == 10:
			scaffolding_input.append(current_row)
			current_row = ""
		else:
			current_row += chr(c)
	scaffolding = Field.create_from_input(scaffolding_input[:-1], Cell)
	scaffolding.print()
	return sum(scaffolding.gen_cells(
		filterer=lambda c: c.value == "#" and scaffolding.apply_adjacent(
			c,
			False,
			filterer=lambda n: n.value == "#"
		) == 4,
		transform=lambda c: c.x * c.y,
	))
