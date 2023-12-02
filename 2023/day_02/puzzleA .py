from __future__ import annotations
from pathlib import Path
import re
from dataclasses import dataclass

DATA_FILE_NAME = "input.txt"
INPUT_FILE = Path(__file__).parent / DATA_FILE_NAME
DATA_TEST_FILE_NAME = "example_1.txt"
TEST_INPUT_FILE = Path(__file__).parent / DATA_TEST_FILE_NAME


@dataclass
class GrabRound:
    red: int
    green: int
    blue: int

    def __le__(self, other: GrabRound):
        return (
            self.red <= other.red
            and self.green <= other.green
            and self.blue <= other.blue
        )


class Game:
    def __init__(self, id: int, plays: list[GrabRound]) -> None:
        self.id = id
        self.plays = plays


def parse_input(file_path: Path) -> list[Game]:
    with open(file_path) as file:
        games = []
        for raw_line in file:
            line = raw_line.strip()
            # Separate game id from plays
            id_part, plays_part = line.split(":")
            id = int(id_part[4:])
            # Parse each round
            rounds = []
            round_parts = plays_part.split(";")
            for round_part in round_parts:
                cube_grabs_parts = round_part.split(",")
                red = 0
                green = 0
                blue = 0
                for cube_grab_part in cube_grabs_parts:
                    cube_grab_part = cube_grab_part.strip()
                    value, color = cube_grab_part.split(" ")
                    if color == "red":
                        red = int(value)
                    elif color == "green":
                        green = int(value)
                    elif color == "blue":
                        blue = int(value)
                    else:
                        raise Exception(f"wrong color: {color}")
                rounds.append(GrabRound(red, green, blue))
            games.append(Game(id, rounds))

    return games


def solve_01(data: list[Game]) -> int:
    control_round = GrabRound(red=12, green=13, blue=14)
    sum = 0
    for game in data:
        possible_game = True
        for round in game.plays:
            if not round <= control_round:
                possible_game = False
        if possible_game:
            sum += game.id
    return sum


def main() -> None:
    data = parse_input(INPUT_FILE)
    solution = solve_01(data)
    print(solution)


if __name__ == "__main__":
    main()
