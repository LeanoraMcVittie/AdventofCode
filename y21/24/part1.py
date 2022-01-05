from typing import Callable, List
from functools import partial
from random import random

class ALU:
    def __init__(self, instructions: List[str]) -> None:
        self.instructions = instructions
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.input = []

    def reset(self) -> None:
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0

    def run(self) -> None:
        i = 0
        for instuction in self.instructions:
            try:
                instr, vs = instuction.split(" ", 1)
                {
                    "inp": self.inp,
                    "add": partial(self.op, lambda a, b: a + b),
                    "mul": partial(self.op, lambda a, b: a * b),
                    "div": partial(self.op, lambda a, b: int(a / b)),
                    "mod": partial(self.op, lambda a, b: a % b),
                    "eql": self.eql,
                }[instr](*vs.split(" "))
            except OverflowError: import pdb; pdb.set_trace()

    def set_input(self, input_args: List[int]) -> None:
        self.input = input_args

    def _save(self, var: str, val: int) -> None:
        if var == "w":
            self.w = val
        elif var == "x":
            self.x = val
        elif var == "y":
            self.y = val
        elif var == "z":
            self.z = val
        else: raise ValueError(f"invalid variable: {var}")

    def _load(self, var: str) -> int:
        try:
            return {
                "w": self.w,
                "x": self.x,
                "y": self.y,
                "z": self.z,
            }[var]
        except KeyError: return int(var)

    def inp(self, var: str) -> None:
        self.print()
        print()
        self._save(var, self.input[0])
        self.input = self.input[1:]

    def op(self, transform: Callable, var: str, b: str) -> None:
        self._save(
            var,
            transform(
                self._load(var),
                self._load(b),
            )
        )

    def eql(self, var: str, b: str) -> None:
        self._save(
            var,
            1 if self._load(var) == self._load(b) else 0,
        )

    def print(self) -> None:
        print(f"w: {self.w}")
        print(f"x: {self.x}")
        print(f"y: {self.y}")
        print(f"z: {self.z}")


def sum_digits(val: int) -> int:
    return sum(int(d) for d in str(val))


def run(input_data: List[str]) -> int:
    alu = ALU(input_data)
    # for i in range(99999999999999, -1, -1):
    i = 99999999999999
    while i > 11111111111110:
    # 	i = int(random() * 100000000000000)
        stringified = str(i)
        if str(i).count("0") > 0 or i < 10000000000000:
        # if i < 10000000000000:
            i -= 1
            continue
        print(i)
        print(sum_digits(i))
        alu.set_input([int(c) for c in str(i)])
        alu.run()
        alu.print()
        if alu.z == 0:
            return i
        a = int(input() or 1)
        if a > 10000000000000: i = a
        else: i -= a
        alu.reset()
