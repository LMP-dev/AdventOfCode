from pathlib import Path
import re
from dataclasses import dataclass

DATA_FILE_NAME = "input.txt"
INPUT_FILE = Path(__file__).parent / DATA_FILE_NAME
DATA_TEST_FILE_NAME = "example_1.txt"
TEST_INPUT_FILE = Path(__file__).parent / DATA_TEST_FILE_NAME


@dataclass
class CubeGrab:
    red: int
    green: int
    blue: int


class Game:
    def __init__(self, id: int, plays: list[CubeGrab]) -> None:
        self.id = id
        self.plays = plays


def parse_input(file_path: Path) -> list[Game]:
    with open(file_path) as file:
        games = []
        for raw_line in file:
            line = raw_line.strip()
            id_pattern = "Game (\d+):"
    return games


def is_it_a_number(character: str) -> tuple[bool, int | str]:
    try:
        number = int(character)
    except ValueError:
        return (False, character)
    else:
        return (True, number)


def solve_01(data: list[str]) -> int:
    return


def main() -> None:
    data = parse_input(TEST_INPUT_FILE)
    solution = solve_01(data)
    print(solution)


if __name__ == "__main__":
    main()
