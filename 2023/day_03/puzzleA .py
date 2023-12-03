from pathlib import Path

DATA_FILE_NAME = "input.txt"
INPUT_FILE = Path(__file__).parent / DATA_FILE_NAME
DATA_TEST_FILE_NAME = "example_1.txt"
TEST_INPUT_FILE = Path(__file__).parent / DATA_TEST_FILE_NAME


def parse_input(file_path: Path) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def solve_01(data: list[str]) -> int:
    part_numbers = []

    return sum(part_numbers)


def main() -> None:
    data = parse_input(TEST_INPUT_FILE)
    solution = solve_01(data)
    print(solution)


if __name__ == "__main__":
    main()
