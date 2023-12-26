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


NEXT_STEP_OFFSETS: dict[Direction, tuple[int, int]] = {
    Direction.RIGTH: (0, 1),
    Direction.UP: (-1, 0),
    Direction.LEFT: (0, -1),
    Direction.DOWN: (1, 0),
}


def add_tuples(one: tuple[int, int], other: tuple[int, int]) -> tuple[int, int]:
    return (one[0] + other[0], one[1] + other[1])


@dataclass(frozen=True)
class State:
    location: tuple[int, int]
    facing: Direction

    def next_state(self, mirror: str) -> list[State]:
        match mirror:
            case ".":
                return [State(self._next_location(), self.facing)]
            case "-" if self.facing in (Direction.RIGTH, Direction.LEFT):
                return [State(self._next_location(), self.facing)]
            case "|" if self.facing in (Direction.UP, Direction.DOWN):
                return [State(self._next_location(), self.facing)]
            case "/":
                if self.facing == Direction.RIGTH:
                    new_facing = Direction.UP
                if self.facing == Direction.UP:
                    new_facing = Direction.RIGTH
                if self.facing == Direction.LEFT:
                    new_facing = Direction.DOWN
                if self.facing == Direction.DOWN:
                    new_facing = Direction.LEFT
                return [State(self._next_location(new_facing), new_facing)]
            case "\\":
                if self.facing == Direction.RIGTH:
                    new_facing = Direction.DOWN
                if self.facing == Direction.DOWN:
                    new_facing = Direction.RIGTH
                if self.facing == Direction.LEFT:
                    new_facing = Direction.UP
                if self.facing == Direction.UP:
                    new_facing = Direction.LEFT
                return [State(self._next_location(new_facing), new_facing)]
            case "-":  # Already considered case passing through
                new_facings = (Direction.LEFT, Direction.RIGTH)
                return [
                    State(self._next_location(new_facing), new_facing)
                    for new_facing in new_facings
                ]
            case "|":  # Already considered case passing through
                new_facings = (Direction.UP, Direction.DOWN)
                return [
                    State(self._next_location(new_facing), new_facing)
                    for new_facing in new_facings
                ]
            case _:
                raise Exception(
                    f"Cannot calculate next step from {self}, and mirror {mirror}"
                )

    def _next_location(self, new_facing: Direction = None) -> tuple[int, int]:
        if new_facing:
            offset = NEXT_STEP_OFFSETS[new_facing]
        else:
            offset = NEXT_STEP_OFFSETS[self.facing]
        return add_tuples(self.location, offset)


@dataclass
class Beam:
    row: int
    col: int
    direction: Direction
    visited_tiles: list[tuple[tuple[int, int], Direction]] = field(default_factory=list)

    def __post_init__(self):
        if not self.visited_tiles:
            self.visited_tiles.append(((self.row, self.col), self.direction))

    def move(self, mirror_map: Grid, max_row, max_col) -> tuple[bool, list[Beam]]:
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
        mirror = mirror_map[(next_row, next_col)]
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


Grid = dict[tuple[int, int], str]


def parse_input(file_content: list[str]) -> Grid:
    grid = dict()
    for r, line in enumerate(file_content):
        # Parse lines and add extra expanded rows when all "."
        row = list(line)
        grid.update({(r, c): char for c, char in enumerate(row)})
    return grid


def solve_01(data: Grid) -> int:
    visited: set[State] = set()
    queue: list[State] = [State((0, 0), Direction.RIGTH)]

    while queue:
        current_state = queue.pop()
        if current_state in visited:
            continue

        visited.add(current_state)

        next_states = current_state.next_state(data[current_state.location])
        for next_state in next_states:
            # Check state is inside grid
            if next_state.location in data:
                queue.append(next_state)

    energized_tiles = {state.location for state in visited}

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
    print(f"The solution of the part 1 is {solution}")  # Wrong solution 8406


if __name__ == "__main__":
    main()
