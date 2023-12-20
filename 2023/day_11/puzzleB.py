# Standard library
from pathlib import Path

INPUT_FILE_PATH = Path(__file__).parent


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> tuple[list[list[str]], int, int]:
    to_expand_row_indexes = []
    to_expand_column_indexes = []
    grid: list[list[str]] = []
    for r, line in enumerate(file_content):
        # Parse lines and add extra expanded rows when all "."
        row = list(line)
        if row.count(".") == len(row):
            to_expand_row_indexes.append(r)
        grid.append(row)

    # Find expanding columns
    indexes_to_exapnd = []
    for c, _ in enumerate(line):
        column = [row[c] for row in grid]
        if column.count(".") == len(column):
            to_expand_column_indexes.append(c)

    return grid, to_expand_row_indexes, to_expand_column_indexes


def find_galaxies_positions(universe: list[list[str]]) -> list[tuple[int, int]]:
    galaxies: list[tuple[int, int]] = []
    for r, row in enumerate(universe):
        for c, item in enumerate(row):
            if item == "#":
                galaxies.append((r, c))
    return galaxies


def expand_galaxy_coordinates(
    galaxies_coordinates: list[tuple[int, int]],
    rows_to_expand: list[int],
    columns_to_expand: list[int],
) -> list[tuple[int, int]]:
    EXPANSION = 100
    new_galaxies_coordinates = []
    for galaxy in galaxies_coordinates:
        r, c = galaxy
        lower_r = [_ for _ in rows_to_expand if _ < r]
        lower_C = [_ for _ in columns_to_expand if _ < c]
        new_coordinates = (r + EXPANSION * len(lower_r), c + EXPANSION * len(lower_C))
        new_galaxies_coordinates.append(new_coordinates)
    return new_galaxies_coordinates


def create_galaxy_pairs(
    galaxies: list[tuple[int, int]]
) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    pairs = []
    while len(galaxies) != 1:
        galaxy = galaxies.pop()
        for other_galaxy in galaxies:
            pairs.append((galaxy, other_galaxy))
    return pairs


def find_distance_between_galaxies(
    origin: tuple[int, int], dest: tuple[int, int]
) -> int:
    v_dist = abs(dest[0] - origin[0])
    h_dist = abs(dest[1] - origin[1])
    return v_dist + h_dist


def solve_01(data: list[list[str]]) -> int:
    original_universe, rows_to_expand, columns_to_expand = data
    paths_sum = 0
    original_galaxies_coordinates = find_galaxies_positions(original_universe)
    galaxies_coordinates = expand_galaxy_coordinates(
        original_galaxies_coordinates, rows_to_expand, columns_to_expand
    )
    galaxy_pairs = create_galaxy_pairs(galaxies_coordinates)
    for pair in galaxy_pairs:
        path_lenght = find_distance_between_galaxies(pair[0], pair[1])
        paths_sum += path_lenght
    return paths_sum


def main() -> None:
    # input.txt | example_1.txt | example_1_v2.txt
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
