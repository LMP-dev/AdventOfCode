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

    def next_blocks(self) -> list[CityBlock]:
        next_directions = Direction._member_names_.remove(self.coming_from)

        # Check 3 consecutive paths
        ...

        return


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]):
    return


def solve_01(data) -> int:
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
