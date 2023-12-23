# Standard library
from pathlib import Path

INPUT_FILE_PATH = Path(__file__).parent


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines

coord = tuple[int,int]

def parse_input(file_content: list[str]) ->tuple[list[coord], list[coord], int, int]:
    round_rocks = []
    cube_rocks = []
    for r, line in enumerate(file_content):
        for c, space in enumerate(line):
            if space == "O":
                round_rocks.append((r,c))
            elif space == "#":
                cube_rocks.append((r,c))
    max_r = r
    max_c = c

    return round_rocks, cube_rocks, max_r, max_c

def organize_rocks_by_columns(round_rocks: list[coord], cube_rocks: list[coord], max_col:int) -> dict[int,dict[str,list[int]]]:
    platform = {}
    for col in range(max_col+1):
        platform.update({col:{"round":[], "cube":[]}})
    for rock in round_rocks:
        r,c = rock
        platform[c]["round"].append(r)
    for rock in cube_rocks:
        r,c = rock
        platform[c]["cube"].append(r)
    return platform



def create_row_sections(separation_points: list[int], max_value: int) -> list[tuple[int,int]]:
    ini = -1
    sections = []
    for point in separation_points:
        sections.append((ini, point))
        ini = point
    sections.append((ini,max_value+1))
    return sections

def spread_between_sections(sections:list[tuple[int,int]], all_values: list[int]) -> dict[tuple[int,int], list[int]]:
    filled_sections = {}
    for section in sections:
        values = [val for val in all_values if val > section[0] and val < section[1]]
        filled_sections.update({section: values})
    return filled_sections

def reorder_section_north(section: tuple[int,int], values: list[int]) -> list[int]:
    new_values = []
    occupied_pos = section[0]
    for _ in values:
        new_values.append(occupied_pos + 1)
        occupied_pos += 1
    return new_values


def tilt_north_column(rows_round_rocks: list[int], rows_cube_rocks:[list[int]], max_col:int) -> list[int]:
    '''Needs row coordinates for 1 column of the platform'''
    new_rows_round_rocks = []
    row_sections = create_row_sections(rows_cube_rocks, max_col)
    filled_row_sections = spread_between_sections(row_sections, rows_round_rocks)
    for section, rock_row_coords in filled_row_sections.items():
        new_rock_row_coords = reorder_section_north(section, rock_row_coords)
        new_rows_round_rocks.extend(new_rock_row_coords)
    return new_rows_round_rocks

def count_column_load(rocks_rows_in_column: list[int], max_row: int) -> int:
    load = 0
    for rock in rocks_rows_in_column:
        load += max_row + 1 - rock
    return load

def perform_cycle(platform):
    ...

def solve_01(data) -> int:
    total_load = 0

    round_rocks, cube_rocks, max_r, max_c = data
    column_platform = organize_rocks_by_columns(round_rocks, cube_rocks, max_c)

    new_column_platform = {}
    for col, rocks in column_platform.items():
        new_round_rocks = tilt_north_column(rocks["round"],rocks["cube"], max_c)
        new_column_platform.update({col: {"round": new_round_rocks, "cube": rocks["cube"]}})

        total_load += count_column_load(new_round_rocks, max_r)
        
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
