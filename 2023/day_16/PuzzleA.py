# Standard library
from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum, auto

INPUT_FILE_PATH = Path(__file__).parent


class OutOfBoundsException(Exception):
    pass


class Direction(Enum):
    UP = auto()
    RIGTH = auto()
    DOWN = auto()
    LEFT = auto()


@dataclass
class Beam:
    row: int
    col: int
    direction: Direction
    visited_tiles: list[tuple[tuple[int, int], Direction]] = field(default_factory=list)

    def __post_init__(self):
        if not self.visited_tiles:
            self.visited_tiles.append(((self.row, self.col), self.direction))

    def move(
        self, mirror_map: list[list[str]], max_row, max_col
    ) -> tuple[bool, list[Beam]]:
        # Find next position
        try:
            next_row, next_col = self._next_position_coordinates(max_row, max_col)
        except OutOfBoundsException:
            return False, [self]

        # Check if already visited position
        tile = ((next_row, next_col), self.direction)
        if tile in self.visited_tiles:
            return False, [self]

        # Find direction in new tile
        mirror = mirror_map[next_row][next_col]
        new_direction = self._change_direction(mirror)
        if isinstance(new_direction, tuple):
            new_beams = []
            for dir in new_direction:
                beam = Beam(next_row, next_col, dir, visited_tiles=self.visited_tiles)
                beam.visited_tiles.append(tile)
                new_beams.append(beam)
            return True, new_beams
        else:
            self.update_state(next_row, next_col, new_direction)
            self.visited_tiles.append(tile)
            return True, [self]

    def update_state(self, row: int, col: int, dir: Direction) -> None:
        self.row = row
        self.col = col
        self.direction = dir

    def _next_position_coordinates(self, max_row: int, max_col: int) -> tuple[int, int]:
        if self.direction == Direction.RIGTH:
            next_row = self.row
            next_col = self.col + 1
        elif self.direction == Direction.UP:
            next_row = self.row - 1
            next_col = self.col
        elif self.direction == Direction.LEFT:
            next_row = self.row
            next_col = self.col - 1
        elif self.direction == Direction.DOWN:
            next_row = self.row + 1
            next_col = self.col
        else:
            raise Exception(f"Unknown direction: {self.direction}")

        # Check position still inside bounds
        if next_row == -1 or next_col == -1 or next_row > max_row or next_col > max_col:
            raise OutOfBoundsException
        else:
            return next_row, next_col

    def _change_direction(self, mirror: str) -> Direction | tuple[Direction, Direction]:
        if mirror == ".":
            return self.direction
        elif mirror == "/":
            if self.direction == Direction.RIGTH:
                return Direction.UP
            if self.direction == Direction.UP:
                return Direction.RIGTH
            if self.direction == Direction.LEFT:
                return Direction.DOWN
            if self.direction == Direction.DOWN:
                return Direction.LEFT
        elif mirror == "\\":  # TODO check with parsing it correctly in grid
            if self.direction == Direction.RIGTH:
                return Direction.DOWN
            if self.direction == Direction.DOWN:
                return Direction.RIGTH
            if self.direction == Direction.LEFT:
                return Direction.UP
            if self.direction == Direction.UP:
                return Direction.LEFT
        elif mirror == "|":
            if self.direction == Direction.RIGTH or self.direction == Direction.LEFT:
                return Direction.DOWN, Direction.UP
            if self.direction == Direction.DOWN or self.direction == Direction.UP:
                return self.direction
        elif mirror == "-":
            if self.direction == Direction.RIGTH or self.direction == Direction.LEFT:
                return self.direction
            if self.direction == Direction.DOWN or self.direction == Direction.UP:
                return Direction.RIGTH, Direction.LEFT


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> tuple[list[list[str]], int, int]:
    grid: list[list[str]] = []
    max_row = None
    max_col = None
    for r, line in enumerate(file_content):
        # Parse lines and add extra expanded rows when all "."
        row = list(line)
        grid.append(row)
    max_row = r
    max_col = len(row) - 1
    return grid, max_row, max_col


def solve_01(data: tuple[list[list[str]], int, int]) -> int:
    mirrors, max_r, max_c = data
    energized_tiles = set()

    beams_moving: list[Beam] = [Beam(0, 0, Direction.RIGTH)]
    beams_end_travel: list[Beam] = []

    # Make the beam travel through the mirrors
    while beams_moving:
        beam = beams_moving.pop()
        is_new_tile, beams = beam.move(mirrors, max_r, max_c)
        if is_new_tile:
            beams_moving.extend(beams)
        else:
            beams_end_travel.extend(beams)

    # Calculate the energized tiles
    for beam in beams_end_travel:
        tiles = [visited[0] for visited in beam.visited_tiles]
        energized_tiles.update(tiles)

    return len(energized_tiles)


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
