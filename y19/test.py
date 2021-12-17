from typing import List
from intcode import IntCode

class TestFailureException(Exception):
    pass

def get_input() -> List[str]:
	with open(f"y19/intcode_test_input.txt", 'r') as input_file:
		values: List[str] = input_file.readlines()
	return [v.strip() for v in values]


def io_test(memory, program_input, expected_output) -> None:
    computer = IntCode(memory, program_input)
    computer.run()
    if computer.outputs[0] != expected_output:
        raise TestFailureException(f"ouput: {computer.outputs[0]} did not match expected output: {expected_output}")


if __name__ == "__main__":
    input_data = get_input()

    # instruction tests
    i = 1
    while input_data[i] != "":
        memory, expected_output = input_data[i].split(" -> ")
        print(f"Testing: {memory}")
        expected_output = [int(c) for c in expected_output.split(",")]
        computer = IntCode(memory)
        computer.run()
        if computer.codes != expected_output:
            print("Something's not right")
            print("Input:")
            print(memory)
            print()
            print("Expected:")
            print(expected_output)
            print()
            print("Actual:")
            print(computer.codes)
            print()
            raise TestFailureException()
        i += 1

    i += 2
    while i < len(input_data) and input_data[i] != "":
        memory, extra = input_data[i].split(" -> ")
        print(f"Testing: {memory}")
        tests, expected_behavior = extra.split(" // ")
        for test in tests.split(","):
            program_input, expected_output = test.split(":")
            print(f"    input: {program_input}, expected output: {expected_output}")
            try:
                io_test(memory, int(program_input), int(expected_output))
            except TestFailureException as e:
                print(f"Expected behavior: {expected_behavior}")
                print("Starting memory:")
                print(memory)
                print()
                raise e
        i += 1

    print("All tests passed!")
