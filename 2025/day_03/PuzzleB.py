# Standard library
from pathlib import Path
from typing import Any

INPUT_FILE_PATH = Path(__file__).parent

DIGITS = 12


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> Any:
    battery_banks: list[int] = []
    for line in file_content:
        battery_banks.append([int(c) for c in line])
    return battery_banks


def find_biggest_number_and_index(row: list[int], min_size: int) -> tuple[int, int]:
    digit, index = None, None

    if min_size == 0:
        adapted_row = row
    else:
        adapted_row = row[:-min_size]

    for i, num in enumerate(adapted_row):
        if num == 9:
            digit = num
            index = i
            break  # Stop at first highest possible number
        elif digit is None:
            digit = num
            index = i
        elif num > digit:
            digit = num
            index = i

    return digit, index


def find_joltage(row_num: list[int], digits: int) -> int:
    joltage = 0
    index = -1

    # Initial loops
    for size in reversed(range(1, digits)):
        battery_num, new_index = find_biggest_number_and_index(
            row_num[index + 1 :], size
        )

        index += new_index + 1
        joltage += battery_num * (10**size)

    # Last loop
    battery_num, _ = find_biggest_number_and_index(row_num[index + 1 :], 0)
    joltage += battery_num

    return joltage


def solve_02(data: Any) -> int:
    joltages = []

    for bank in data:
        joltages.append(find_joltage(bank, DIGITS))

    return sum(joltages)


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the example 1 is {solution}")  # Solution 3121910778619
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the part 2 is {solution}")  # Solution 170520923035051

    # file_content = read_data(INPUT_FILE_PATH / "test.txt")
    # data = parse_input(file_content)
    # solution = solve_02(data)
    # print(f"The solution of the example 1 is {solution}")  # Solution 999765432211


if __name__ == "__main__":
    main()
