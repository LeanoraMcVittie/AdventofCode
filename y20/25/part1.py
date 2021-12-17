from typing import List


def find_loop_size(pk: int) -> int:
	value = 1
	i = 0
	while value != pk:
		value *= 7
		value %= 20201227
		i += 1
	return i

def tranform_pk(pk: int, loop_size: int) -> int:
	value = 1
	for i in range(loop_size):
		value *= pk
		value %= 20201227
	return value

def run(input_data: List[str]) -> int:
	card_pk = int(input_data[0])
	door_pk = int(input_data[1])
	card_loop_size = find_loop_size(card_pk)
	door_loop_size = find_loop_size(door_pk)
	transformed_card_pk = tranform_pk(card_pk, door_loop_size)
	transformed_door_pk = tranform_pk(door_pk, card_loop_size)
	if transformed_card_pk != transformed_door_pk:
		raise Exception("something went wrong")
	return transformed_card_pk
