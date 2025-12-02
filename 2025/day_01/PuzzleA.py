# Standard library
from pathlib import Path
from typing import Any
from dataclasses import dataclass

INPUT_FILE_PATH = Path(__file__).parent


@dataclass
class Dial:
    lower: int = 0
    higher: int = 99
    current: int = 50

    zero_count: int = 0

    def find_0s(self, instructions: list[tuple[str, int]]) -> int:
        for direction, number in instructions:
            if direction == "R":
                self._move_right(number)
            if direction == "L":
                self._move_left(number)

        return self.zero_count

    def _move_left(self, positions: int): ...

    def _move_right(self, positions: int): ...


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> list[tuple[str, int]]:
    instructions = [(line[0], int(line[1:])) for line in file_content]
    return instructions


def solve_01(data: Any) -> int:
    dial = Dial()

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
