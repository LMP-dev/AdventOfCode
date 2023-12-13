# Standard library
from pathlib import Path
from dataclasses import dataclass
from enum import Enum, auto

# 3rd party libraries
import numpy as np

INPUT_FILE_PATH = Path(__file__).parent

class Direction(Enum):
    NORD = auto()
    EAST = auto()
    SUD = auto()
    WEST = auto()

@dataclass
class Move:



def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> tuple[list[list[str]], tuple[int, int]]:
    matrix = []
    for r, grid_line in enumerate(file_content):
        new_row = []
        for c, char in enumerate(grid_line):
            new_row.append(char)
            if char == "S":
                start_position = (r, c)
        matrix.append(new_row)
    return matrix, start_position


def solve_01(data: tuple[list[list[str]], tuple[int, int]]) -> int:
    # Unpack data
    grid, start_position = data
    step = 0
    st = np.array(start_position)

    next_step_moves = [()]
    # nord_route = {"active": True, "path": []}
    # east_route = {"active": True, "path": []}
    # south_route = {"active": True, "path": []}
    # west_route = {"active": True, "path": []}


    positions = [data[1]]
    visited_positions = []

    while True:


    return step


def main() -> None:
    # input.txt | example_1.txt | example_1_v2.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the example 1 is {solution}")
    file_content = read_data(INPUT_FILE_PATH / "example_2.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the example 2 is {solution}")
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the part 1 is {solution}")


if __name__ == "__main__":
    main()
