from typing import List
from y19.intcode import IntCode, OutputClear


class Game:
	def __init__(self, computer_code: str) -> None:
		self.computer = IntCode(computer_code)
		self.tiles = {}

	def play_game(self) -> None:
		self.computer.run()

	def mark_tiles(self) -> None:
		try:
			while True:
				x = self.computer.next_output()
				y = self.computer.next_output()
				tile_id = self.computer.next_output()
				self.tiles[(x,y)] = tile_id
		except OutputClear: pass
		return list(self.tiles.values()).count(2)

def run(input_data: List[str], **kwargs) -> int:
	game = Game(input_data[0])
	game.play_game()
	return game.mark_tiles()
