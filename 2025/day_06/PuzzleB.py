# Standard library
from pathlib import Path

INPUT_FILE_PATH = Path(__file__).parent


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.rstrip("\n") for line in file]  # normally .strip()
    return lines


def parse_input(file_content: list[str]) -> tuple[list[list[int]], list[str]]:
    operators: list[str] = file_content[-1].split()
    numbers_to_operate: list[list[int]] = []

    # temp variable reseated each operation
    group_of_numbers: list[int] = []

    for i, _ in enumerate(file_content[0]):
        # Read cephalopod by columns
        group = [line[i] for line in file_content[:-1]]
        # Check end of operation
        if all(x == " " for x in group):
            numbers_to_operate.append(group_of_numbers)
            group_of_numbers = []
            continue
        # Create number
        num_str = ""
        for character in group:
            if character == " ":
                continue
            else:
                num_str += character
        group_of_numbers.append(int(num_str))
    # Last number treatment
    numbers_to_operate.append(group_of_numbers)

    if len(operators) != len(numbers_to_operate):
        raise Exception("DIFFERENT length in list to operate!")

    return numbers_to_operate, operators


def solve_02(data: tuple[list[list[int]], list[str]]) -> int:
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
    print(f"The solution of the example 1 is {solution}")  # Solution 3263827
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the part 2 is {solution}")  # Solution 11044319475191


if __name__ == "__main__":
    main()
