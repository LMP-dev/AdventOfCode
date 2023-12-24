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
    return


def hash_algorithm(sequence: str) -> int:
    current_value = 0

    for char in sequence:
        # Determine ASCII code
        asci = ord(char)
        # Increase current value by ASCII code
        current_value += asci
        # Multiply current value by 17
        current_value *= 17
        # Set to reminder divinding by 256
        current_value %= 256
    return current_value


def solve_02(data: Any) -> int:
    return


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
