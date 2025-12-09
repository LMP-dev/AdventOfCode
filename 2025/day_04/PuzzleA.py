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


def parse_input(file_content: list[str]) -> tuple[list[tuple[int, int]], int, int]:
    """Returns a set with coordinates with paper and max row and max column"""
    cells_with_paper = []

    for i, line in enumerate(file_content):
        for j, char in enumerate(line):
            if char == "@":
                cells_with_paper.append((i, j))
    max_row = i
    max_col = j

    return cells_with_paper, max_row, max_col


def check_accessible_roll(
    cell: tuple[int, int], map: list[tuple[int, int]], max_row: int, max_col: int
) -> bool:
    count = 0
    max_count = 3

    # Top cell --> move row -
    if cell[0] - 1 < 0:
        t_cell = None
    else:
        t_cell = (cell[0] - 1, cell[1])
    # Top-right cell --> move row - and col +
    if cell[0] - 1 < 0 or cell[1] + 1 > max_col:
        tr_cell = None
    else:
        tr_cell = (cell[0] - 1, cell[1] + 1)
    # Right cell --> move col +
    if cell[1] + 1 > max_col:
        r_cell = None
    else:
        r_cell = (cell[0], cell[1] + 1)
    # Bottom-right cell --> move row + and col +
    if cell[0] + 1 > max_col or cell[1] + 1 > max_row:
        br_cell = None
    else:
        br_cell = (cell[0] + 1, cell[1] + 1)
    # Bottom cell --> move row +
    if cell[0] + 1 > max_row:
        b_cell = None
    else:
        b_cell = (cell[0] + 1, cell[1])
    # Bottom-left cell --> move row + and col -
    if cell[0] + 1 > max_row or cell[1] - 1 < 0:
        bl_cell = None
    else:
        bl_cell = (cell[0] + 1, cell[1] - 1)
    # Left cell --> move col -
    if cell[1] - 1 < 0:
        l_cell = None
    else:
        l_cell = (cell[0], cell[1] - 1)
    # Top-left cell --> move row - and col -
    if cell[0] - 1 < 0 or cell[1] - 1 < 0:
        tl_cell = None
    else:
        tl_cell = (cell[0] - 1, cell[1] - 1)
    neighbour_cells = [
        t_cell,
        tr_cell,
        r_cell,
        br_cell,
        b_cell,
        bl_cell,
        l_cell,
        tl_cell,
    ]
    valid_neighbours = [cell for cell in neighbour_cells if cell is not None]

    for cell in valid_neighbours:
        if cell in map:
            count += 1
            if count > max_count:
                return False
    return True


def solve_01(data: Any) -> int:
    cells_with_paper, max_row, max_col = data
    count = 0

    for cell in cells_with_paper:
        if check_accessible_roll(cell, cells_with_paper, max_row, max_col):
            count += 1

    return count


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
