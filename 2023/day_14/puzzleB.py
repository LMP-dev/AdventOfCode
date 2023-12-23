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


def spin_cycle(reflector: rock_platform.Platform) -> None:
    """Tilt North - West - South - East"""
    # North tilt
    reflector_state = reflector.organize_rocks_by_column()
    new_round_rocks = []
    for col, rocks in reflector_state.items():
        new_rocks = operations.tilt_platform(
            rocks[Shape.ROUND], rocks[Shape.CUBE], reflector.max_col
        )
        new_rocks_coords = [(row, col) for row in new_rocks]
        new_round_rocks.extend(new_rocks_coords)
    reflector.update_round_rocks(new_round_rocks)

    # West tilt
    reflector_state = reflector.organize_rocks_by_row()
    new_round_rocks = []
    for row, rocks in reflector_state.items():
        new_rocks = operations.tilt_platform(
            rocks[Shape.ROUND], rocks[Shape.CUBE], reflector.max_row
        )
        new_rocks_coords = [(row, col) for col in new_rocks]
        new_round_rocks.extend(new_rocks_coords)
    reflector.update_round_rocks(new_round_rocks)

    # South tilt
    reflector_state = reflector.organize_rocks_by_column()
    new_round_rocks = []
    for col, rocks in reflector_state.items():
        new_rocks = operations.tilt_platform(
            rocks[Shape.ROUND], rocks[Shape.CUBE], reflector.max_col, inverse_order=True
        )
        new_rocks_coords = [(row, col) for row in new_rocks]
        new_round_rocks.extend(new_rocks_coords)
    reflector.update_round_rocks(new_round_rocks)

    # East tilt
    reflector_state = reflector.organize_rocks_by_row()
    new_round_rocks = []
    for row, rocks in reflector_state.items():
        new_rocks = operations.tilt_platform(
            rocks[Shape.ROUND], rocks[Shape.CUBE], reflector.max_row, inverse_order=True
        )
        new_rocks_coords = [(row, col) for col in new_rocks]
        new_round_rocks.extend(new_rocks_coords)
    reflector.update_round_rocks(new_round_rocks)


def find_cycle_pattern(reflector: rock_platform.Platform) -> tuple[int, int]:
    """Reflector ends in the state that starts the pattern"""
    previous_spins = [reflector.get_copy_object()]
    cycle = 0
    while True:
        spin_cycle(reflector)
        new_reflector = reflector.get_copy_object()
        if new_reflector in previous_spins:
            break
        else:
            previous_spins.append(new_reflector)
            cycle += 1

    index = previous_spins.index(new_reflector)

    return index, cycle + 1


def solve_01(data) -> int:
    total_of_cycles = 1000000000

    round_rocks, cube_rocks, max_r, max_c = data
    reflector = rock_platform.Platform(round_rocks, cube_rocks, max_r, max_c)

    # Find cycle pattern
    cycle_origin, cycle_end = find_cycle_pattern(
        reflector
    )  # cycle 0 is originial position
    cycle_pattern = cycle_end - cycle_origin

    # Remove cycles until arriving to pattern:
    cycles_to_do = total_of_cycles - (cycle_origin - 1)

    # Remove complete cycles of the pattern:
    cycles_to_do = cycles_to_do % cycle_pattern

    # Perform remaining cycles until total
    for _ in range(cycles_to_do - 1):  # -1 due to alredy at start of pattern
        spin_cycle(reflector)

    rock_rows = reflector.get_rock_rows()

    return count_column_load(rock_rows, max_r)


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
