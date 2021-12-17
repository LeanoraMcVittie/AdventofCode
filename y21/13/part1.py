from typing import List


def run(input_data: List[str]) -> int:
	coordinates = []
	i = 0
	while input_data[i] != "":
		x, y = input_data[i].split(",")
		x = int(x)
		y = int(y)
		coordinates.append((x,y))
		i += 1
	i += 1
	while i < len(input_data):
		axis, val = input_data[i][11:].split("=")
		val = int(val)
		new_coordinates = []
		for x, y in coordinates:
			if axis == "x" and x > val:
				new_x = val - (x - val)
				if not (new_x,y) in new_coordinates:
					new_coordinates.append((new_x,y))
			elif axis == "y" and y > val:
				new_y = val - (y - val)
				if not (x,new_y) in new_coordinates:
					new_coordinates.append((x,new_y))
			elif (x,y) not in new_coordinates:
				new_coordinates.append((x,y))
		coordinates = new_coordinates
		i += 1
		return len(coordinates)
