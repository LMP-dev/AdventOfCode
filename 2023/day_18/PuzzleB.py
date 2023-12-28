# Standard library
from pathlib import Path
from typing import Any

INPUT_FILE_PATH = Path(__file__).parent


MOVEMENT: dict[str, tuple[int, int]] = {
    "R": (0, 1),
    "U": (-1, 0),
    "L": (0, -1),
    "D": (1, 0),
}


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input_old(file_content: list[str]) -> list[tuple[str, int]]:
    instructions = []
    for line in file_content:
        dir, steps, _ = line.split(" ")
        instructions.append((dir, int(steps)))
    return instructions


def parse_input(file_content: list[str]) -> list[tuple[str, int]]:
    """return a list with: Direction(str) | steps(int)"""
    DIRECTIONS = {0: "R", 1: "D", 2: "L", 3: "U"}
    instructions = []
    for line in file_content:
        _, _, hexa_code = line.split(" ")
        hexa_number = hexa_code[1:-2]
        num_direction = hexa_code[-1]
        instructions.append((DIRECTIONS[num_direction], int(hexa_number, 16)))
    return instructions


def add_tuples(one: tuple[int, int], other: tuple[int, int]) -> tuple[int, int]:
    return (one[0] + other[0], one[1] + other[1])


def find_min_coordinates(
    current_min_coords: tuple[int, int], new_trenches: list[tuple[int, int]]
) -> tuple[int, int]:
    min_row_coords = [current_min_coords[0]].extend(
        [trench[0] for trench in new_trenches]
    )
    min_col_coords = [current_min_coords[1]].extend(
        [trench[1] for trench in new_trenches]
    )
    return min(min_row_coords), min(min_col_coords)


def advance_one_direction(
    position: tuple[int, int], direction: str, steps: int
) -> tuple[int, int]:
    movement = MOVEMENT[direction]
    distance = (movement[0] * steps, movement[1] * steps)
    return add_tuples(position, distance)


def generate_digged_trench_corners(
    starting_pos: tuple[int, int], instructions: list[tuple[str, int]]
) -> dict[tuple[int, int], list[tuple[int, int]]]:
    loop_corners: dict[tuple[int, int], list[tuple[int, int]]] = {starting_pos: []}
    current_pos = starting_pos
    for instruction in instructions:
        direction, steps = instruction
        new_pos = advance_one_direction(current_pos, direction, steps)
        loop_corners[current_pos].append(new_pos)
        loop_corners.update[{new_pos: [current_pos]}]
    return loop_corners  # TODO check initial pos correctly updated


def solve_02(data: list[tuple[str, int]]) -> int:
    loop_trenches = generate_digged_trench_corners((0, 0), data)

    # Follow instructions to generate all corners coordinates

    # Normalise coordinates to know the initial rectangle

    # Remove the area of the non-digged rectangles

    return


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input_old(file_content)
    solution = solve_02(data)
    print(f"The solution of the example 1 is {solution}")
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input_old(file_content)
    solution = solve_02(data)
    print(f"The solution of the part 2 is {solution}")


if __name__ == "__main__":
    main()
