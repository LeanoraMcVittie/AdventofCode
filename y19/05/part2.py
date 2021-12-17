from typing import List
from y19.intcode import IntCode

def run(input_data: List[str]) -> int:
	computer = IntCode(input_data[0], 5)
	computer.run()
	outputs = computer.outputs
	diagnostic_code = outputs.pop(-1)
	if not outputs:
		return diagnostic_code
	print(outputs)
