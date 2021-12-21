from typing import Callable, Generator, List
from functools import partial


# This shows the state of IntCode at the time of solving day 7


class WaitingOnInput(Exception):
    pass


class Halted(Exception):
    pass


class IntCode:
    def __init__(self, memory_str: str, program_input__DEPRECATED: int = None) -> None:
        self.codes = [int(i) for i in memory_str.split(",")]
        self.ip = 0
        self.input = [program_input__DEPRECATED] if program_input__DEPRECATED else []
        self.outputs = []
        self.halted = False
        self.output_gen = self.gen_output()

    def add_input(self, new_input: int) -> None:
        self.input.append(new_input)

    def next_output(self) -> int:
        return next(self.output_gen)

    def gen_output(self) -> Generator[int, None, None]:
        i = 0
        while True:
            yield self.outputs[i]
            i += 1

    def run(self) -> None:
        if self.halted:
            raise Halted()

        while self.codes[self.ip] != 99:
            self.modes = list(str(int(self.codes[self.ip]/100)).zfill(3))
            {
                1: partial(self.operator, lambda x, y: x + y),
                2: partial(self.operator, lambda x, y: x * y),
                3: self.save_input,
                4: self.output,
                5: partial(self.jump, False),
                6: partial(self.jump, True),
                7: partial(self.compare, lambda x, y: x < y),
                8: partial(self.compare, lambda x, y: x == y),
            }[self.codes[self.ip]%100]()

        self.halted = True

    def load(self, index: int) -> int:
        return self.codes[self.codes[index]] if self.modes.pop() == "0" else self.codes[index]

    def save(self, index: int, value: int) -> int:
        self.modes.pop()
        self.codes[self.codes[index]] = value

    def operator(self, transform: Callable) -> None:
        value = transform(self.load(self.ip+1), self.load(self.ip+2))
        self.save(self.ip+3, value)
        self.ip += 4

    def save_input(self) -> None:
        if len(self.input) == 0:
            raise WaitingOnInput()
        self.save(self.ip+1, self.input.pop(0))
        self.ip += 2

    def output(self) -> None:
        self.outputs.append(self.load(self.ip+1))
        self.ip += 2

    def jump(self, on_zero: bool) -> None:
        is_zero = self.load(self.ip+1) == 0
        if (on_zero and is_zero) or (not on_zero and not is_zero):
            self.ip = self.load(self.ip+2)
        else:
            self.ip += 3

    def compare(self, comparator: Callable) -> None:
        store = 1 if comparator(self.load(self.ip+1), self.load(self.ip+2)) else 0
        self.save(self.ip+3, store)
        self.ip += 4
