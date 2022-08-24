from typing import Callable, Generator, List
from functools import partial


# Intcode problems: 02, 05, 07, 09, 11, 13, 15


class WaitingOnInput(Exception):
    pass


class Halted(Exception):
    pass


class OutputClear(Exception):
    pass


class IO:
    def __init__(self) -> None:
        self.io = []
        self.it = 0

    def add(self, item: int) -> None:
        self.io.append(item)

    def next(self) -> int:
        if self.it >= len(self.io):
            raise self.ExceptionType()
        n = self.io[self.it]
        self.it += 1
        return n

    def get(self, index) -> int:
        assert index < len(self.io)
        return self.io[index]


class Output(IO):
    ExceptionType = OutputClear


class Input(IO):
    ExceptionType = WaitingOnInput


class IntCode:
    def __init__(self, memory_str: str) -> None:
        self.memory = {
            i: int(memory_str.split(",")[i]) for i in range(len(memory_str.split(",")))
        }
        self.ip = 0
        self.rb = 0
        self.input = Input()
        self.output = Output()
        self.halted = False

    def add_input(self, new_input: int) -> None:
        self.input.add(new_input)

    def next_output(self) -> int:
        return self.output.next()

    def last_output(self) -> int:
        return self.output.get(-1)

    def run(self) -> None:
        if self.halted:
            raise Halted()

        while self.memory[self.ip] != 99:
            self.modes = list(str(int(self.memory[self.ip] / 100)).zfill(3))
            {
                1: partial(self.operator, lambda x, y: x + y),
                2: partial(self.operator, lambda x, y: x * y),
                3: self.store_input,
                4: self.add_output,
                5: partial(self.jump, lambda x: x != 0),
                6: partial(self.jump, lambda x: x == 0),
                7: partial(self.compare, lambda x, y: x < y),
                8: partial(self.compare, lambda x, y: x == y),
                9: self.base,
            }[self.memory[self.ip] % 100]()

        self.halted = True

    def _load(self, loc: int) -> int:
        return self.memory.setdefault(loc, 0)

    def load(self, index: int) -> int:
        mode = self.modes.pop()
        if mode == "0":
            return self._load(self.memory[index])
        elif mode == "1":
            return self._load(index)
        elif mode == "2":
            return self._load(self.rb + self.memory[index])
        else:
            raise ValueError(f"{mode} is not a valid mode")

    def store(self, index: int, value: int) -> int:
        mode = self.modes.pop()
        if mode == "0":
            self.memory[self.memory[index]] = value
        elif mode == "2":
            self.memory[self.rb + self.memory[index]] = value
        else:
            raise ValueError(f"{mode} is not a valid mode for writing")

    def operator(self, transform: Callable) -> None:
        value = transform(self.load(self.ip + 1), self.load(self.ip + 2))
        self.store(self.ip + 3, value)
        self.ip += 4

    def store_input(self) -> None:
        self.store(self.ip + 1, self.input.next())
        self.ip += 2

    def add_output(self) -> None:
        self.output.add(self.load(self.ip + 1))
        self.ip += 2

    def jump(self, condition: Callable, num_args: int = 1) -> None:
        args = [self.load(self.ip + i) for i in range(1, num_args + 1)]
        if condition(*args):
            self.ip = self.load(self.ip + num_args + 1)
        else:
            self.ip += num_args + 2

    def compare(self, comparator: Callable) -> None:
        store = 1 if comparator(self.load(self.ip + 1), self.load(self.ip + 2)) else 0
        self.store(self.ip + 3, store)
        self.ip += 4

    def base(self) -> None:
        self.rb += self.load(self.ip + 1)
        self.ip += 2
