from typing import List


class SeatSimulation:
	seat_map: List[List[str]]
	new_map: List[List[str]]
	num_rows: int 
	num_cols: int 

	def __init__(self, input_map: List[str]) -> None:
		self.seat_map = [list(row) for row in input_map]
		self.num_rows = len(self.seat_map)
		self.num_cols = len(self.seat_map[0])
		self.new_map = [[c for c in r] for r in self.seat_map]

	def print_map(self, m) -> None:
		for row in m:
			print(str.join("", row))

	def _occupied_adjacent_seats(self, row: int, col: int):
		occupied = 0
		for i in range(row-1, row+2):
			if i < 0 or i >= self.num_rows:
				continue
			for j in range(col-1, col+2):
				if j < 0 or j >= self.num_cols:
					continue
				if self.seat_map[i][j] == "#":
					occupied += 1
		return occupied

	def _occupied_star_seats(self, row: int, col: int):
		occupied = 0
		try:	
			# check row left
			for i in range(col-1, -1, -1):
				if self.seat_map[row][i] == "#":
					occupied += 1
					break
				if self.seat_map[row][i] == "L":
					break
			for i in range(col+1, self.num_cols):
				if self.seat_map[row][i] == "#":
					occupied += 1
					break
				if self.seat_map[row][i] == "L":
					break
			# check col
			for i in range(row-1, -1, -1):
				if self.seat_map[i][col] == "#":
					occupied += 1
					break
				if self.seat_map[i][col] == "L":
					break
			for i in range(row+1, self.num_rows):
				if self.seat_map[i][col] == "#":
					occupied += 1
					break
				if self.seat_map[i][col] == "L":
					break
			# check first diagonal
			curr_row = row 
			for i in range(col-1, -1, -1):
				curr_row -= 1
				if curr_row < 0:
					continue
				if self.seat_map[curr_row][i] == "#":
					occupied += 1
					break
				if self.seat_map[curr_row][i] == "L":
					break
			curr_row = row
			for i in range(col+1, self.num_cols):
				curr_row += 1 
				if curr_row >= self.num_rows:
					break
				if self.seat_map[curr_row][i] == "#":
					occupied += 1
					break
				if self.seat_map[curr_row][i] == "L":
					break
			# check second diagonal
			curr_row = row 
			for i in range(col-1, -1, -1):
				curr_row += 1
				if curr_row >= self.num_rows:
					continue
				if self.seat_map[curr_row][i] == "#":
					occupied += 1
					break
				if self.seat_map[curr_row][i] == "L":
					break
			curr_row = row
			for i in range(col+1, self.num_cols):
				curr_row -= 1 
				if curr_row < 0:
					break
				if self.seat_map[curr_row][i] == "#":
					occupied += 1
					break
				if self.seat_map[curr_row][i] == "L":
					break
		except IndexError:
			import pdb; pdb.set_trace()
		return occupied

	def _run_one_round(self) -> bool:
		changed = False
		for i in range(0, self.num_rows):
			for j in range(0, self.num_cols):
				if self.seat_map[i][j] == ".":
					self.new_map[i][j] = "."
				elif self.seat_map[i][j] == "#":
					if self._occupied_star_seats(i, j) >= 5:
						self.new_map[i][j] = "L"
						changed = True
					else:
						self.new_map[i][j] = "#"
				else:
					if self._occupied_star_seats(i, j) == 0:
						self.new_map[i][j] = "#"
						changed = True
					else:
						self.new_map[i][j] = "L"
		# import pdb; pdb.set_trace()
		self.seat_map = [[c for c in r] for r in self.new_map]
		return changed

	def run_simulation(self) -> None:
		while True:
			if not self._run_one_round():
				return

	def count_occupied(self) -> int:
		occupied = 0
		for i in range(0, self.num_rows):
			for j in range(0, self.num_cols):
				if self.seat_map[i][j] == "#":
					occupied += 1
		return occupied


def run(input_data: List[str]) -> int:
	seat_simulation = SeatSimulation(input_data)
	seat_simulation.run_simulation()
	return seat_simulation.count_occupied()