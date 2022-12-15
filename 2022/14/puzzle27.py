from pathlib import Path

import numpy as np

INPUT_FILE = Path(__file__).parent / "input.txt"
# INPUT_FILE = Path(__file__).parent / "test_input.txt"
SAND_COL_START = 500


def calculate_points_in_line(start: tuple[int], end: tuple[int]) -> set[int]:
    """Only for horizontal and vertical lines."""
    points = set([start, end])
    # vertical lines
    if start[0] == end[0]:
        for i in range(abs(start[1] - end[1]) - 1):
            if start[1] < end[1]:
                next_point = (start[0], start[1] + i + 1)
            elif start[1] > end[1]:
                next_point = (start[0], start[1] - i - 1)
            points.update(set([next_point]))
    # horizontal line
    elif start[1] == end[1]:
        for i in range(abs(start[0] - end[0]) - 1):
            if start[0] < end[0]:
                next_point = (start[0] + i + 1, start[1])
            elif start[0] > end[0]:
                next_point = (start[0] - i - 1, start[1])
            points.update(set([next_point]))
    return points


def parse_line_rocks(line: str, lowest_col: int) -> tuple[set[(tuple[int])], int]:
    """Calculate all rocks coordinates and updates lowest column coordinate"""
    points_line = set()
    pos_line = line.strip().split(" -> ")
    # Previous point to know line direction
    last_row = None
    last_col = None
    for pos in pos_line:
        col, row = map(int, pos.split(","))
        if not last_row:
            last_row = row
            last_col = col
            # For boundary values
            lowest_col = col
            highest_col = col
            max_row = row
        else:
            points_line.update(
                calculate_points_in_line((last_row, last_col), (row, col))
            )
            if col < lowest_col:
                lowest_col = col
            if col > highest_col:
                highest_col = col
            if row > max_row:
                max_row = row
            last_row = row
            last_col = col
    return points_line, lowest_col, highest_col, max_row


def find_rock_positions(file_path: Path) -> tuple[list[tuple[int]], int]:
    """
    Returns a list with the coordinates of rocks and the shape of the grid to be used."""
    rocks = set()
    lowest_col_coordinate = float("inf")
    max_col_coordinate = float("-inf")
    max_row_coordinate = float("-inf")
    with open(file_path, "r") as file:
        for line in file:
            coord_rocks, lowest_col, highest_col, max_row = parse_line_rocks(
                line, lowest_col_coordinate
            )
            rocks.update(coord_rocks)
            if lowest_col < lowest_col_coordinate:
                lowest_col_coordinate = lowest_col
            if highest_col > max_col_coordinate:
                max_col_coordinate = highest_col
            if max_row > max_row_coordinate:
                max_row_coordinate = max_row
    return rocks, lowest_col_coordinate, max_col_coordinate, max_row_coordinate


def move_sand_grain(grid: np.ndarray, starting_column: int) -> tuple[bool, tuple[int]]:
    """Returns if the grain is still moving and the final position"""
    moving = True
    pos = (0, starting_column)
    while moving:
        down_pos = (pos[0] + 1, pos[1])
        down_left_pos = (pos[0] + 1, pos[1] - 1)
        down_right_pos = (pos[0] + 1, pos[1] + 1)
        try:
            down_occupied = grid[down_pos]
        except IndexError:
            break
        if not down_occupied:
            pos = down_pos
            continue
        # Down is occupied, we try down-left
        if down_left_pos[1] == -1:
            break
        down_left_occupied = grid[down_left_pos]
        if not down_left_occupied:
            pos = down_left_pos
            continue
        # Down-left is also occupied, we try down-right
        try:
            down_right_occupied = grid[down_right_pos]
        except IndexError:
            break
        if not down_right_occupied:
            pos = down_right_pos
            continue
        moving = False
    return moving, pos


def main() -> None:
    rocks_pos, min_col, max_col, max_row = find_rock_positions(INPUT_FILE)
    grid_shape = (max_row + 1, max_col - min_col + 1)
    grid = np.zeros(grid_shape)
    for rock in rocks_pos:
        updated_rock_pos = (rock[0], rock[1] - min_col)
        grid[updated_rock_pos] = 1

    while True:
        # Sand grain starts moving
        moving, final_pos = move_sand_grain(grid, SAND_COL_START - min_col)
        if moving:
            break
        grid[final_pos] = 2

    # print(grid)
    sand_grains = grid[grid == 2]
    print(f"number of grains is {len(sand_grains)}")


if __name__ == "__main__":
    main()
