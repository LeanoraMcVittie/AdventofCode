from typing import List
from y19.intcode import IntCode

def run(input_data: List[str], **kwargs) -> int:
	computer = IntCode(input_data[0])
	computer.add_input(2)
	computer.run()
	return computer.next_output()
