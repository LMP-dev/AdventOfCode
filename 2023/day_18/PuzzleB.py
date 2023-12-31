# Standard library
from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass

INPUT_FILE_PATH = Path(__file__).parent

STARTING_POS = (0, 0)
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


def advance_one_direction(
    position: tuple[int, int], direction: str, steps: int
) -> tuple[int, int]:
    movement = MOVEMENT[direction]
    distance = (movement[0] * steps, movement[1] * steps)
    return add_tuples(position, distance)


def generate_digged_trench_corners(
    starting_pos: tuple[int, int], instructions: list[tuple[str, int]]
) -> dict[tuple[int, int], list[tuple[int, int]]]:
    # Initialize variables
    current_corner = starting_pos
    loop_corners: dict[tuple[int, int], list[tuple[int, int]]] = {current_corner: []}
    # Populate corners graph
    for instruction in instructions:
        direction, steps = instruction
        new_corner = advance_one_direction(current_corner, direction, steps)
        loop_corners[current_corner].append(new_corner)
        if new_corner != starting_pos:
            loop_corners.update({new_corner: [current_corner]})
        else:  # Special case end of loop
            loop_corners[starting_pos].append(current_corner)
        current_corner = new_corner
    return loop_corners


def find_min_max_coordinates(
    trenches: list[tuple[int, int]],
) -> tuple[tuple[int, int], tuple[int, int]]:
    min_row = STARTING_POS[0]
    min_col = STARTING_POS[1]
    max_row = STARTING_POS[0]
    max_col = STARTING_POS[1]
    for trench in trenches:
        min_row = min(min_row, trench[0])
        min_col = min(min_col, trench[1])
        max_row = max(max_row, trench[0])
        max_col = max(max_col, trench[1])
    return (min_row, min_col), (max_row, max_col)


def normalize_list_coordinates(
    coords_list: list[tuple[int, int]], vector: tuple[int, int]
) -> list[tuple[int, int]]:
    return [add_tuples(coord, vector) for coord in coords_list]


def normalize_graph_coordinates(
    graph: dict[tuple[int, int], list[tuple[int, int]]], vector: tuple[int, int]
) -> dict[tuple[int, int], list[tuple[int, int]]]:
    return {
        add_tuples(k, vector): normalize_list_coordinates(v, vector)
        for k, v in graph.items()
    }


def solve_02(data: list[tuple[str, int]]) -> int:
    # Follow instructions to generate all corners coordinates
    corners_graph = generate_digged_trench_corners(STARTING_POS, data)

    # Normalise coordinates to have (0,0) in the top-left corner
    corners_list = corners_graph.keys()
    min_coordinates, max_coordinates = find_min_max_coordinates(corners_list)
    vector = (-min_coordinates[0], -min_coordinates[1])
    normalized_corners_graph = normalize_graph_coordinates(corners_graph, vector)
    norm_max_coordinates = add_tuples(max_coordinates, vector)

    # Remove the area of the non-digged rectangles
    total_area = (norm_max_coordinates[0] + 1) * (norm_max_coordinates[1] + 1)
    # Left vertical side

    return total_area


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input_old(file_content)
    solution = solve_02(data)
    print(f"The solution of the example 1 is {solution}")
    # file_content = read_data(INPUT_FILE_PATH / "input.txt")
    # data = parse_input_old(file_content)
    # solution = solve_02(data)
    # print(f"The solution of the part 2 is {solution}")


if __name__ == "__main__":
    main()
