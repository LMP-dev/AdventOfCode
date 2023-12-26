# Standard library
from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum, auto

INPUT_FILE_PATH = Path(__file__).parent


class Direction(Enum):
    RIGHT = auto()
    TOP = auto()
    LEFT = auto()
    DOWN = auto()


@dataclass
class CityBlock:
    loc: tuple[int, int]
    coming_from: Direction
    heat_loss: int
    followed_path: list[CityBlock] = field(default_factory=list)

    def next_blocks(self, grid: Grid) -> list[CityBlock]:
        next_directions = Direction._member_names_.remove(self.coming_from)

        # Check 3 consecutive paths
        ...

        # Check still inside grid

        return


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


Grid: dict[tuple[int, int], int]


def parse_input(file_content: list[str]) -> Grid:
    grid = dict()
    for r, line in enumerate(file_content):
        # Parse lines and add extra expanded rows when all "."
        row = list(line)
        grid.update({(r, c): char for c, char in enumerate(row)})
    return grid


def distance_funct(block: CityBlock) -> int:
    """Calculates distance for search algorithm"""
    return CityBlock.heat_loss


def solve_01(data) -> int:
    queue: list[CityBlock] = [CityBlock((0, 0), Direction.RIGHT, data[(0, 0)])]
    visited: list[tuple(int, int)] = []

    while queue:
        # Sort according to heat loss
        queue.sort(key=distance_funct)
        current_block = queue.pop(0)

        if current_block.loc in visited:
            continue
        visited.append(current_block.loc)

        queue.extend(current_block.next_blocks)
        ...

    # CityBlock have a record of path visited (calculate heat loss of path)

    return


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the example 1 is {solution}")
    # file_content = read_data(INPUT_FILE_PATH / "input.txt")
    # data = parse_input(file_content)
    # solution = solve_01(data)
    # print(f"The solution of the part 1 is {solution}")


if __name__ == "__main__":
    main()
