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


def parse_input(file_content: list[str]) -> tuple[list[list[int], list[str]]]:
    numbers: list[list[int]] = []
    operators = None

    # Parse line of numbers and store each line
    for i, line in enumerate(file_content):
        if i == len(file_content) - 1:
            operators = line.split()
        else:
            numbers.append(line.split())

    numbers_to_operate: list[list[int]] = []
    # Create tuples of each numerand
    for index, _ in enumerate(operators):
        numbers_to_operate.append([int(nums[index]) for nums in numbers])

    return numbers_to_operate, operators


def solve_01(data: tuple[list[list[int], list[str]]]) -> int:
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
    solution = solve_01(data)
    print(f"The solution of the example 1 is {solution}")  # Solution 4277556
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the part 1 is {solution}")  # Solution 6417439773370


if __name__ == "__main__":
    main()
