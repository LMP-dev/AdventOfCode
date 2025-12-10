# Standard library
from pathlib import Path
from functools import cache

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


@cache
def identify_valid_neighbours(
    cell: tuple[int, int], max_row: int, max_col: int
) -> list[tuple[int, int]]:
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

    return valid_neighbours


def check_accessible_roll(
    cell: tuple[int, int], map: list[tuple[int, int]], max_row: int, max_col: int
) -> bool:
    count = 0
    max_count = 3

    valid_neighbours = identify_valid_neighbours(cell, max_row, max_col)

    for cell in valid_neighbours:
        if cell in map:
            count += 1
            if count > max_count:
                return False
    return True


def identify_cells_next_round(
    cell: tuple[int, int], map: set[tuple[int, int]], max_row: int, max_col: int
) -> list[tuple[int, int]]:
    valid_neighbours = identify_valid_neighbours(cell, max_row, max_col)

    cells_with_paper = []

    for cell in valid_neighbours:
        if cell in map:
            cells_with_paper.append(cell)

    return cells_with_paper


def solve_02(data: tuple[list[tuple[int, int]], int, int]) -> int:
    cells_with_paper, max_row, max_col = data
    count = 0
    changes_last_round = True

    cells_to_review: set[tuple[int, int]] = set(cells_with_paper.copy())

    iter = 0
    while changes_last_round:
        cells_to_remove = []
        for cell in cells_to_review:
            if check_accessible_roll(cell, cells_with_paper, max_row, max_col):
                count += 1
                cells_to_remove.append(cell)

        if cells_to_remove:
            # Remove this round papers
            for cell in cells_to_remove:
                cells_with_paper.remove(cell)
            # Identify cells to review
            next_cells = []
            for cell in cells_to_remove:
                next_cells.extend(
                    identify_cells_next_round(cell, cells_with_paper, max_row, max_col)
                )
            cells_to_review = set(next_cells)
        else:
            changes_last_round = False

    return count


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the example 1 is {solution}")  # Solution 43
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the part 2 is {solution}")  # Solution 8727 (slow!)


if __name__ == "__main__":
    main()
