from pathlib import Path
from dataclasses import dataclass
import math

INPUT_FILE_PATH = Path(__file__).parent


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> list[tuple[int, int]]:
    return


def solve_01(data: list[int]) -> int:
    seeds, finder = data
    # variables initialization
    minimum_location = math.inf
    for seed in seeds:
        location = finder.get_location(seed)
        minimum_location = min(minimum_location, location)

    return minimum_location


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the example is {solution}")
    data = parse_input(INPUT_FILE_PATH / "input.txt")
    solution = solve_01(data)  # 25004
    print(f"The solution of part 1 is {solution}")


if __name__ == "__main__":
    main()
