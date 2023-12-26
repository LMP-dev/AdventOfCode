# Standard library
from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum, auto
from functools import cached_property

INPUT_FILE_PATH = Path(__file__).parent


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


def parse_input(file_content: list[str]) -> tuple[Grid, int, int]:
    grid = dict()
    for r, line in enumerate(file_content):
        # Parse lines and add extra expanded rows when all "."
        row = list(line)
        grid.update({(r, c): char for c, char in enumerate(row)})
    max_row = r
    max_col = len(row) - 1
    return grid, max_row, max_col


def generate_initial_positions(max_row, max_col) -> list[State]:
    positions: list[State] = []

    left_side = [State((r, 0), Direction.RIGTH) for r in range(max_row + 1)]
    down_side = [State((max_row, c), Direction.UP) for c in range(max_col + 1)]
    right_side = [State((r, max_col), Direction.LEFT) for r in range(max_row + 1)]
    up_side = [State((0, c), Direction.DOWN) for c in range(max_col + 1)]

    positions.extend(left_side)
    positions.extend(down_side)
    positions.extend(right_side)
    positions.extend(up_side)

    return positions


def find_energized_tiles(
    initial_pos: State, mirrors: dict[tuple[int, int], str]
) -> int:
    visited: set[State] = set()
    queue: list[State] = [initial_pos]

    while queue:
        current_state = queue.pop()
        if current_state in visited:
            continue

        visited.add(current_state)

        next_states = current_state.next_state(mirrors[current_state.location])
        for next_state in next_states:
            # Check state is inside grid
            if next_state.location in mirrors:
                queue.append(next_state)

    energized_tiles = {state.location for state in visited}
    return len(energized_tiles)


def solve_02(data: tuple[Grid, int, int]) -> int:
    mirrors, max_r, max_c = data
    max_energized_tiles = 0
    for initial_pos in generate_initial_positions(max_r, max_c):
        num_energized_tiles = find_energized_tiles(initial_pos, mirrors)
        max_energized_tiles = max(max_energized_tiles, num_energized_tiles)

    return max_energized_tiles


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the example 1 is {solution}")
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the part 2 is {solution}")  # Solution 8389


if __name__ == "__main__":
    main()
