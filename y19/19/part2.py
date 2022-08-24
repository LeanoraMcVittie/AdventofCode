from typing import List
from y19.intcode import IntCode


def is_in_tractor_beam(program: str, x: int, y: int) -> bool:
    tractor_beam = IntCode(program)
    tractor_beam.add_input(x)
    tractor_beam.add_input(y)
    tractor_beam.run()
    return tractor_beam.next_output() == 1


def run(input_data: List[str]) -> int:
    program = input_data[0]
    x = 0
    y = 0
    while not is_in_tractor_beam(program, x + 99, y):
        y += 1
        while not is_in_tractor_beam(program, x, y + 99):
            x += 1
    return x * 10000 + y
