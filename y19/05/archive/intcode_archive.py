from typing import Callable, List
from functools import partial


# The state of IntCode after solving day 5


class IntCode:
    def __init__(self, memory_str: str, program_input: int = None) -> None:
        self.codes = [int(i) for i in memory_str.split(",")]
        self.ip = 0
        self.input = program_input
        self.outputs = []

    def run(self) -> None:
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
        self.save(self.ip+1, self.input)
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
