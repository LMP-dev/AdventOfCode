# Standard library
from pathlib import Path
from dataclasses import dataclass

INPUT_FILE_PATH = Path(__file__).parent


MOVEMENT: dict[str, tuple[int, int]] = {
    "R": (0, 1),
    "U": (-1, 0),
    "L": (0, -1),
    "D": (1, 0),
}


@dataclass
class Trench:
    position: tuple[int, int]
    color: str

    def translate(self, movement: tuple[int, int]) -> None:
        self.position = add_tuples(self.position, movement)


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> list[tuple[str, int, str]]:
    instructions = []
    for line in file_content:
        dir, steps, color = line.split(" ")
        instructions.append((dir, int(steps), color[1:-1]))
    return instructions


def add_tuples(one: tuple[int, int], other: tuple[int, int]) -> tuple[int, int]:
    return (one[0] + other[0], one[1] + other[1])


def dig_trenches(
    current_pos: tuple[int, int], direction: str, steps: int, color: str
) -> tuple[list[Trench], tuple[int, int]]:
    trenches = []
    offset = MOVEMENT[direction]
    for _ in range(steps):
        current_pos = add_tuples(current_pos, offset)
        trenches.append(Trench(current_pos, color))
    return trenches, current_pos


def next_dig_locations(position: tuple[int, int]) -> list[tuple[int, int]]:
    return [
        add_tuples(position, movement)
        for movement in [(1, 0), (0, 1), (-1, 0), (0, -1)]
    ]


def dig_inside_trenches_loop(
    trenches: list[Trench], inside_pos: tuple[int, int]
) -> set[tuple[int, int]]:
    """returns all the digged positions (both trenches and inside)"""
    digged: set[tuple(int, int)] = {trench.position for trench in trenches}
    to_dig: list(tuple(int, int)) = [inside_pos]

    # Simple check for initial position not on trench
    if inside_pos in digged:
        raise Exception(
            f"The initial inside_position {inside_pos} is already on top of the trench loop! CHoose a new initial position"
        )

    while to_dig:
        hole = to_dig.pop()
        digged.add(hole)
        new_dig_locations = next_dig_locations(hole)
        for next_hole in new_dig_locations:
            if next_hole in digged or next_hole in to_dig:
                continue
            else:
                to_dig.append(next_hole)
    return digged


def find_min_coordinates(
    current_min_coords: tuple[int, int], new_trenches: list[Trench]
) -> tuple[int, int]:
    min_row_coords = [current_min_coords[0]]
    min_col_coords = [current_min_coords[1]]
    min_row_coords.extend([trench.position[0] for trench in new_trenches])
    min_col_coords.extend([trench.position[1] for trench in new_trenches])
    return min(min_row_coords), min(min_col_coords)


def solve_01(data: list[tuple[str, int, str]]) -> int:
    current_pos = (0, 0)
    loop_trenches: list[Trench] = []
    min_coords = (0, 0)

    # Dig loop trenches
    for instruction in data:
        direction, steps, color = instruction
        new_trenches, current_pos = dig_trenches(current_pos, direction, steps, color)
        loop_trenches.extend(new_trenches)
        min_coords = find_min_coordinates(min_coords, new_trenches)

    # Normalize loop coordinates
    norm_loop_trenches_pos = [
        add_tuples(trench.position, (-min_coords[0], -min_coords[1]))
        for trench in loop_trenches
    ]

    # Find initial position inside the loop for the second digging cycle
    norm_loop_trenches_pos.sort()
    first_row = [
        pos for pos in norm_loop_trenches_pos if pos[0] == norm_loop_trenches_pos[0][0]
    ]
    inside_loop_pos = add_tuples(first_row[0], (1, 1))
    # Dig inside loop
    digged_holes = dig_inside_trenches_loop(loop_trenches, inside_loop_pos)

    return len(digged_holes)


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
