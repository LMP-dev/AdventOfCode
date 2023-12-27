# Standard library
from pathlib import Path
from heapq import heappop, heappush
from dataclasses import dataclass
from enum import Enum, auto


INPUT_FILE_PATH = Path(__file__).parent
MIN_MOV = 4
MAX_MOV = 10


class Direction(Enum):
    RIGHT = auto()
    UP = auto()
    LEFT = auto()
    DOWN = auto()


OPPOSITE_DIRECTION = {
    Direction.RIGHT: Direction.LEFT,
    Direction.UP: Direction.DOWN,
    Direction.LEFT: Direction.RIGHT,
    Direction.DOWN: Direction.UP,
}

NEXT_STEP_OFFSETS: dict[Direction, tuple[int, int]] = {
    Direction.RIGHT: (0, 1),
    Direction.UP: (-1, 0),
    Direction.LEFT: (0, -1),
    Direction.DOWN: (1, 0),
}


@dataclass(frozen=True)
class State:
    location: tuple[int, int]
    facing: Direction

    def __lt__(self, other) -> bool:
        if isinstance(other, State):
            return self.location > other.location


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


Grid = dict[tuple[int, int], int]


def parse_input(file_content: list[str]) -> Grid:
    grid = dict()
    for r, line in enumerate(file_content):
        # Parse lines and add extra expanded rows when all "."
        row = list(line)
        grid.update({(r, c): int(value) for c, value in enumerate(row)})
    return grid


def add_tuples(one: tuple[int, int], other: tuple[int, int]) -> tuple[int, int]:
    return (one[0] + other[0], one[1] + other[1])


def solve_02(data) -> int:
    queue: list[tuple[int, State, int]] = [
        (0, State((0, 0), Direction.DOWN), 1),
        (0, State((0, 0), Direction.RIGHT), 1),
    ]
    visited: set[tuple[State, int]] = set()
    finishing_loc = max(data.keys())

    # Dijkstra algorithm
    while queue:
        heat, position, num_steps = heappop(queue)

        # Check if final position achieved and can stop
        if position.location == finishing_loc and num_steps >= MIN_MOV:
            return heat

        # Check if position visited
        if (position, num_steps) in visited:
            continue
        visited.add((position, num_steps))

        # Find allowed new directions and move
        if num_steps < MIN_MOV:  # Can only follow same direction
            direction = position.facing
            next_num_steps = num_steps + 1
            offset = NEXT_STEP_OFFSETS[direction]
            loc = add_tuples(position.location, offset)

            # Check if allowed movement
            if loc not in data:
                continue

            heappush(queue, (heat + data[loc], State(loc, direction), next_num_steps))
        else:
            next_directions: list[Direction] = [
                Direction.RIGHT,
                Direction.UP,
                Direction.LEFT,
                Direction.DOWN,
            ]
            next_directions.remove(OPPOSITE_DIRECTION[position.facing])
            for direction in next_directions:
                if direction == position.facing:  # Check not max movement achieved
                    next_num_steps = num_steps + 1
                    if next_num_steps > MAX_MOV:
                        continue
                else:
                    next_num_steps = 1
                offset = NEXT_STEP_OFFSETS[direction]
                loc = add_tuples(position.location, offset)

                # Check if allowed movement
                if loc not in data:
                    continue

                heappush(
                    queue, (heat + data[loc], State(loc, direction), next_num_steps)
                )


def main() -> None:
    # input.txt | example_1.txt | example_2.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the example 1 is {solution}")
    file_content = read_data(INPUT_FILE_PATH / "example_2.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the example 2 is {solution}")
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the part 2 is {solution}")


if __name__ == "__main__":
    main()
