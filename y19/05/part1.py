from typing import List
from y19.intcode import IntCode, OutputClear

def run(input_data: List[str]) -> int:
	computer = IntCode(input_data[0])
	computer.add_input(1)
	computer.run()
	while True:
		if computer.next_output() != 0: break
	try: computer.next_output()
	except OutputClear: pass
	else: raise Exception("First non-zero output should be last output")
	return computer.last_output()
