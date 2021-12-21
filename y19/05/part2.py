from typing import List
from y19.intcode import IntCode, OutputClear

def run(input_data: List[str]) -> int:
	computer = IntCode(input_data[0])
	computer.add_input(5)
	computer.run()
	output = computer.next_output()
	try: computer.next_output()
	except OutputClear: pass
	else: raise Exception("There should be exactly one output")
	return output
