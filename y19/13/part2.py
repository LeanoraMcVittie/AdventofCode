from typing import List
from y19.intcode import IntCode, WaitingOnInput, Halted, OutputClear
from utils.field.two_d import Field
from time import sleep

class Game:
    def __init__(self, computer_code: str) -> None:
        self.computer = IntCode(computer_code)
        self.computer.memory[0] = 2 # hacky - don't like this :(
        self.tiles = {}
        self.score = 0
        self.max_x = 0
        self.max_y = 0
        self.ball_x = 0
        self.bar_x = 0

    def play_game(self) -> None:
        try:
            while True:
                try:
                    self.computer.run()
                except WaitingOnInput: pass
                self.mark_tiles()
                self.print()
                if self.ball_x < self.bar_x:
                    new_input = -1
                elif self.bar_x < self.ball_x:
                    new_input = 1
                else:
                    new_input = 0
                self.computer.add_input(new_input)
                sleep(0.2)
        except Halted: pass

    def mark_tiles(self) -> None:
        try:
            while True:
                x = self.computer.next_output()
                if x > self.max_x: self.max_x = x

                y = self.computer.next_output()
                if y > self.max_y: self.max_y = y

                tile_id = self.computer.next_output()

                if x == -1 and y == 0: self.score = tile_id
                else: self.tiles[(x,y)] = tile_id

                if tile_id == 4: self.ball_x = x
                if tile_id == 3: self.bar_x = x
        except OutputClear: pass

    def print(self) -> None:
        for y in range(self.max_y, -1, -1):
            for x in range(self.max_x + 1):
                c = {
                    0: " ",
                    1: "█",
                    2: "#",
                    3: "_",
                    4: "⬤",
                }.get(self.tiles[(x,y)], " ")
                print(c, end="")
            print()


def run(input_data: List[str], **kwargs) -> int:
    game = Game(input_data[0])
    game.play_game()
    return game.score
