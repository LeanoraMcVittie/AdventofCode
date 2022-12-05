from typing import List
import itertools as it


class Layer:
	cols = 25
	rows = 6

def run(input_data: List[str], **kwargs) -> int:
	image = input_data[0]
	layers = []

	while len(image) > 0:
		layers.append(image[:Layer.cols*Layer.rows])
		image = image[Layer.cols*Layer.rows:]

	for i in range(Layer.rows):
		for j in range(Layer.cols):
			for layer in layers:
				if layer[i*Layer.cols + j] != "2":
					if layer[i*Layer.cols + j] == "1": c = "█"
					else: c = "."
					print(c, end="")
					break
			else:
				pass
				print(" ")
		print()
