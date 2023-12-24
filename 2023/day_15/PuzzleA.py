# Standard library
from pathlib import Path

INPUT_FILE_PATH = Path(__file__).parent


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> list[str]:
    raw_initialization_sequence = file_content[0]
    initialization_sequence = raw_initialization_sequence.split(",")

    return initialization_sequence


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


def solve_01(data: list[str]) -> int:
    result_sum = 0

    for sequence in data:
        hash_result = hash_algorithm(sequence)
        result_sum += hash_result

    return result_sum


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
