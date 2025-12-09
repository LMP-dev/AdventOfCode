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


def parse_input(file_content: list[str]) -> list[list[str]]:
    diagram = []

    for line in file_content:
        diagram.append([char for char in line])

    return diagram


def solve_02(data: list[list[str]]) -> int:
    # Create dictionary of columns
    end_tachyon = {i: 0 for i in range(len(data[0]))}

    for i, char in enumerate(data[0]):
        if char == "S":
            end_tachyon[i] = 1

    # Calculate timelines for each separator line
    for i in range(2, len(data), 2):
        for j, char in enumerate(data[i]):
            if char == "^":
                timelines = end_tachyon[j]
                end_tachyon[j - 1] += timelines
                end_tachyon[j + 1] += timelines
                end_tachyon[j] = 0

    return sum(end_tachyon.values())


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the example 1 is {solution}")  # Solution 40
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the part 2 is {solution}")  # Solution 20571740188555


if __name__ == "__main__":
    main()
