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
    print(f"The solution of the part 1 is {solution}")  # Solution 8389


if __name__ == "__main__":
    main()
