# Standard library
from pathlib import Path
from typing import Any

INPUT_FILE_PATH = Path(__file__).parent


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> Any:
    numbers: list[list[int]] = []
    operators = None

    # Parse line of numbers and store each line
    for i, line in enumerate(file_content):
        if i == len(file_content) - 1:
            operators = line.split()
        else:
            numbers.append(line.split())

    normal_read_numbers = []
    # Read by columns
    for index, _ in enumerate(operators):
        normal_read_numbers.append([int(nums[index]) for nums in numbers])
    # do not convert

    # Read numbers by celaphod math
    temp_list = []
    # calculate major number
    # add 0 as strings to other comparing relative lengths
    # select new numbers (mid 0 should not be considered?)
    # convert to int

    # TODO
    numbers_to_operate = []

    return normal_read_numbers, operators


def solve_02(data: Any) -> int:
    numbers_to_operate, operators = data
    total = 0

    for numbers, operator in zip(numbers_to_operate, operators):
        if operator == "+":
            total += sum(numbers)
        elif operator == "*":
            result = 1
            for num in numbers:
                result *= num
            total += result

    return total


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the example 1 is {solution}")
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the part 2 is {solution}")


if __name__ == "__main__":
    main()
