from typing import List
from y19.intcode import IntCode

def run(input_data: List[str], **kwargs) -> int:
	computer = IntCode(input_data[0], 1)
	computer.run()
	outputs = computer.outputs
	diagnostic_code = outputs.pop(-1)
	if all(c == 0 for c in outputs):
		return diagnostic_code
	print(outputs)
