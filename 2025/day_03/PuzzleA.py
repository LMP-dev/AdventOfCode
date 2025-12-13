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


def parse_input(file_content: list[str]) -> list[list[int]]:
    battery_banks = []
    for line in file_content:
        battery_banks.append([int(c) for c in line])
    return battery_banks


def find_joltage(row_num: list[int]) -> int:
    first, f_index = None, None
    second = None

    # First digit loop
    for i, num in enumerate(row_num[:-1]):  # do not consider last digit
        if first is None:
            first = num
            f_index = i
        else:
            if num == 9:
                first = num
                f_index = i
                break  # Stop at first highest possible number
            elif num > first:
                first = num
                f_index = i

    # Second digit loop
    for num in row_num[f_index + 1 :]:
        if second is None:
            second = num
        else:
            if num == 9:
                second = num
                break  # Stop at first highest possible number
            elif num > second:
                second = num

    joltage = first * 10 + second
    # print(f"The Joltage is {joltage}")
    return joltage


def solve_01(data: Any) -> int:
    joltages = []
    for bank in data:
        joltages.append(find_joltage(bank))

    return sum(joltages)


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the example 1 is {solution}")
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the part 1 is {solution}")


if __name__ == "__main__":
    main()
