from typing import List
import itertools as it


class Layer:
	cols = 25
	rows = 6

	def __init__(self, layer_str: str) -> None:
		self.layer_str = layer_str

	def num_zeroes(self) -> int:
		return self.layer_str.count("0")

	def result(self) -> int:
		return self.layer_str.count("1") * self.layer_str.count("2")

def run(input_data: List[str]) -> int:
	image = input_data[0]
	layers = []

	while len(image) > 0:
		layers.append(Layer(image[:Layer.cols*Layer.rows]))
		image = image[Layer.cols*Layer.rows:]

	min_zeros = Layer.cols * Layer.rows
	result = 0
	for layer in layers:
		if layer.num_zeroes() < min_zeros:
			min_zeros = layer.num_zeroes()
			result = layer.result()
	return result
