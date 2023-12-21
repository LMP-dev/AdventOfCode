# Standard library
from pathlib import Path

INPUT_FILE_PATH = Path(__file__).parent


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> list[list[str]]:
    grid: list[list[str]] = []
    for line in file_content:
        # Parse lines and add extra expanded rows when all "."
        row = list(line)
        if row.count(".") == len(row):
            grid.append(row)
        grid.append(row)

    # Expand columns
    indexes_to_exapnd = []
    for i, _ in enumerate(line):
        column = [row[i] for row in grid]
        if column.count(".") == len(column):
            indexes_to_exapnd.append(i)
    accumulated_index = 0
    for index in indexes_to_exapnd:
        for row in grid:
            row.insert(index + accumulated_index, ".")
        accumulated_index += 1

    return grid


def find_galaxies_positions(universe: list[list[str]]) -> list[tuple[int, int]]:
    galaxies: list[tuple[int, int]] = []
    for r, row in enumerate(universe):
        for c, item in enumerate(row):
            if item == "#":
                galaxies.append((r, c))
    return galaxies


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
    paths_sum = 0
    galaxies_coordinates = find_galaxies_positions(data)
    galaxy_pairs = create_galaxy_pairs(galaxies_coordinates)
    for pair in galaxy_pairs:
        path_lenght = find_distance_between_galaxies(pair[0], pair[1])
        paths_sum += path_lenght
    return paths_sum


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
