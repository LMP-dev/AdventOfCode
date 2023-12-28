# Standard library
from pathlib import Path
from typing import Any

INPUT_FILE_PATH = Path(__file__).parent


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
    instructions = []
    for line in file_content:
        _, _, hexa_code = line.split(" ")

        # instructions.append((dir, int(steps), color[1:-1]))
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


def solve_02(data: list[tuple[str, int]]) -> int:
    current_pos = (0, 0)
    loop_trenches: dict[tuple[int, int], list[tuple[int, int]]] = dict()
    min_coords = (0, 0)

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
