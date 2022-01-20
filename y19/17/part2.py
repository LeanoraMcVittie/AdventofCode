from typing import List
from y19.intcode import IntCode


# It was much more fun to work this out by hand than to
# try and figure out how to do it programmatically and
# I'm in this for the fun - so I worked it out by hand
def run(input_data: List[str]) -> int:
	vaccuum_robot = IntCode('2' + input_data[0][1:])
	routine = "B,A,B,C,A,C,A,B,C,A"
	A = "L,10,L,8,R,12"
	B = "L,6,R,8,R,12,L,6,L,8"
	C = "L,8,L,10,L,6,L,6"
	assert all(len(x) <= 20 for x in [routine, A, B, C])
	for input_str in [routine, A, B, C, 'n']:
		for c in input_str:
			vaccuum_robot.add_input(ord(c))
		vaccuum_robot.add_input(10) # newline
	vaccuum_robot.run()
	return vaccuum_robot.last_output()
