# Standard library
from pathlib import Path

# py modules
import rock_platform
from rock_platform import Shape
import operations

INPUT_FILE_PATH = Path(__file__).parent


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


coord = tuple[int, int]


def parse_input(file_content: list[str]) -> tuple[list[coord], list[coord], int, int]:
    round_rocks = []
    cube_rocks = []
    for r, line in enumerate(file_content):
        for c, space in enumerate(line):
            if space == "O":
                round_rocks.append((r, c))
            elif space == "#":
                cube_rocks.append((r, c))
    max_r = r
    max_c = c

    return round_rocks, cube_rocks, max_r, max_c


def count_column_load(rocks_rows_in_column: list[int], max_row: int) -> int:
    load = 0
    for rock in rocks_rows_in_column:
        load += max_row + 1 - rock

    return load


def solve_01(data) -> int:
    total_load = 0

    round_rocks, cube_rocks, max_r, max_c = data
    reflector = rock_platform.Platform(round_rocks, cube_rocks, max_r, max_c)

    # Problem A check
    reflector_state = reflector.organize_rocks_by_column()

    new_round_rocks = []
    for rocks in reflector_state.values():
        new_rocks = operations.tilt_platform(
            rocks[Shape.ROUND], rocks[Shape.CUBE], max_c
        )
        new_round_rocks.extend(new_rocks)

        total_load += count_column_load(new_rocks, max_r)

    return total_load


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
