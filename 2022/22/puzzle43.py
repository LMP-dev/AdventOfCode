from pathlib import Path
import time
from collections import deque
from enum import Enum, auto

import numpy as np
import matplotlib.pyplot as plt

INPUT_FILE = Path(__file__).parent / "input.txt"
# INPUT_FILE = Path(__file__).parent / "test_input.txt"  # sol = 5031


class Orientation(Enum):
    RIGTH = auto()
    DOWN = auto()
    LEFT = auto()
    TOP = auto()


class Explorer:
    DIRECTION_PASSW = {
        Orientation.RIGTH: 0,
        Orientation.DOWN: 1,
        Orientation.LEFT: 2,
        Orientation.TOP: 3,
    }

    def __init__(self, row: int, col: int, ori: Orientation) -> None:
        self.row = row
        self.col = col
        self.ori = ori

    def get_next_position(self) -> tuple[int]:
        if self.ori == Orientation.RIGTH:
            return (self.row, self.col + 1)
        elif self.ori == Orientation.LEFT:
            return (self.row, self.col - 1)
        elif self.ori == Orientation.TOP:
            return (self.row - 1, self.col)
        elif self.ori == Orientation.DOWN:
            return (self.row + 1, self.col)
        raise Exception("No orientation found")

    def move_to(self, new_position: tuple[int]) -> None:
        """Change position of the explorer."""
        self.row, self.col = new_position

    def get_password(self) -> int:
        """The final password is the sum of 1000 times the row, 4 times the column, and the facing."""
        return (
            1000 * (self.row + 1) + 4 * (self.col + 1) + self.DIRECTION_PASSW[self.ori]
        )


def find_opposite_position(line: np.ndarray, reverse: bool) -> int:
    """Checks for the first non 2 position (empty) in the given line."""
    if reverse:
        line = np.flip(line)
    for index, val in enumerate(line):
        if val != 2:
            break
    if reverse:
        return len(line) - 1 - index
    return index


class BoardMap:
    """
    Matrix where:
        0 - path
        1 - wall
        2 - empty space
    """

    ROTATION_DIR_R = [
        Orientation.RIGTH,
        Orientation.DOWN,
        Orientation.LEFT,
        Orientation.TOP,
        Orientation.RIGTH,
    ]

    ROTATION_DIR_L = [
        Orientation.RIGTH,
        Orientation.DOWN,
        Orientation.LEFT,
        Orientation.TOP,
    ]

    def __init__(
        self,
        dimensions: (tuple[int]),
        path_tiles: list[tuple[int]],
        wall_tiles: list[tuple[int]],
    ):
        # Create board and fill it
        self.board = np.ones(dimensions) * 2  # 0 - path; 1 - wall and 2 - empty
        self._add_paths(path_tiles)
        self._add_walls(wall_tiles)
        # Position Explorer
        self.explorer = self._position_explorer()
        # Display code
        self.display = np.copy(self.board)
        self.display[(self.explorer.row, self.explorer.col)] = 10
        # self.display_explorer_position()

    def _add_paths(self, path_tiles: list[tuple[int]]) -> None:
        for coordinate in path_tiles:
            self.board[coordinate] = 0

    def _add_walls(self, wall_tiles: list[tuple[int]]) -> None:
        for coordinate in wall_tiles:
            self.board[coordinate] = 1

    def _position_explorer(self) -> Explorer:
        """You begin the path in the leftmost open tile of the top row of tiles."""
        # Default values
        initial_row = 0
        ori = Orientation.RIGTH
        # Calculate column initial value
        for col, val in enumerate(self.board[initial_row]):
            if val == 0:
                y = col
                break
        return Explorer(initial_row, y, ori)

    def _find_opposite_position(
        self, current_position: tuple[int], orientation: Orientation
    ) -> tuple[int]:
        row, col = current_position
        if orientation in [Orientation.RIGTH, Orientation.LEFT]:
            line = self.board[row]
            reverse = False
            if orientation == Orientation.LEFT:
                reverse = True
            new_col = find_opposite_position(line, reverse)
            return (row, new_col)
        elif self.explorer.ori in [Orientation.TOP, Orientation.DOWN]:
            line = self.board[:, col]
            reverse = False
            if orientation == Orientation.TOP:
                reverse = True
            new_row = find_opposite_position(line, reverse)
            return (new_row, col)

    def follow_directions(self, directions: list[int | str]) -> None:
        for direction in directions:
            if isinstance(direction, int):
                # Move forward until rock
                for _ in range(direction):
                    next_position = self.explorer.get_next_position()
                    try:
                        # Check if outside path
                        if self.board[next_position] == 2:
                            next_position = self._find_opposite_position(
                                next_position,
                                self.explorer.ori,
                            )
                        # Check it is not a rock and move
                        if self.board[next_position] == 1:
                            break
                        else:
                            self.display[(self.explorer.row, self.explorer.col)] = 4
                            self.display[next_position] = 5
                            # self.display_explorer_position()
                            self.explorer.move_to(next_position)

                    except IndexError:
                        # Outside of the board
                        next_position = self._find_opposite_position(
                            (self.explorer.row, self.explorer.col),
                            self.explorer.ori,
                        )
                        # Check it is not a rock and move
                        if self.board[next_position] == 1:
                            break
                        else:
                            self.display[(self.explorer.row, self.explorer.col)] = 4
                            self.display[next_position] = 5
                            # self.display_explorer_position()
                            self.explorer.move_to(next_position)
            else:
                # Change facing direction
                if direction == "R":
                    new_ori = self.ROTATION_DIR_R[
                        self.ROTATION_DIR_R.index(self.explorer.ori) + 1
                    ]
                elif direction == "L":
                    new_ori = self.ROTATION_DIR_L[
                        self.ROTATION_DIR_L.index(self.explorer.ori) - 1
                    ]
                self.explorer.ori = new_ori

    def display_explorer_position(self):
        plt.imshow(self.display)
        plt.show()


def parse_input(file_path: Path) -> tuple[list[str], str]:
    """Splits input in raw map and raw directions."""
    with open(file_path, "r") as file:
        raw_input = file.readlines()

    raw_map = [line.strip("\n") for line in raw_input[:-2]]
    raw_directions = raw_input[-1].strip("\n\r")

    return raw_map, raw_directions


def parse_directions(raw_directions: str) -> list[str | int]:
    """directions only contain numbers and L or R letters."""
    directions = deque()
    number = ""
    for char in raw_directions:
        if char in "1234567890":
            # Add to number until R or L is found
            number += char
        else:
            # Store nunmber (if necessary)
            if number:
                directions.append(int(number))
            # Reser number variable
            number = ""
            # Store rotation
            directions.append(char)
    if number:
        directions.append(int(number))
    return directions


def create_board(raw_map: list[str]) -> BoardMap:
    path_tiles = list()  # will have 0
    wall_tiles = list()  # will have 1 (2 for empty tile)
    max_col_index = 0
    for row, line in enumerate(raw_map):
        for col, char in enumerate(line):
            if char == ".":
                path_tiles.append((row, col))
            elif char == "#":
                wall_tiles.append((row, col))
            if col > max_col_index:
                max_col_index = col
    dimension_board = (len(raw_map), max_col_index + 1)
    return BoardMap(dimension_board, path_tiles, wall_tiles)


def main():
    raw_map, raw_directions = parse_input(INPUT_FILE)
    directions = parse_directions(raw_directions)
    password_map = create_board(raw_map)
    password_map.follow_directions(directions)
    # password_map.display_explorer_position()
    part_1 = password_map.explorer.get_password()
    print(part_1)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"--- {(time.time() - start) * 1000} ms ---")
