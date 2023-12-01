from pathlib import Path
import re

DATA_FILE_NAME = "input.txt"
INPUT_FILE = Path(__file__).parent / DATA_FILE_NAME
TEST_INPUT_FILE = Path(__file__).parent / "example_2.txt"


def parse_input(file_path: Path) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def solve_02(data: list[str]) -> int:
    calibration_values = []
    for i, line in enumerate(data):
        first = None
        last = None
        pattern_end = r"(two).*$"
        match = re.search(pattern_end, line)
        if match:
            print(f"Found two in line  {i}: {match.group(1)}")


def main() -> None:
    data = parse_input(TEST_INPUT_FILE)
    solution = solve_02(data)
    print(solution)


if __name__ == "__main__":
    main()
