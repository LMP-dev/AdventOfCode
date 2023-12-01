from pathlib import Path
import time
from collections import deque
from enum import Enum, auto

import numpy as np

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

    def __init__(self, row: int, col: int, ori: Orientation, face_id: int) -> None:
        self.row = row
        self.col = col
        self.ori = ori
        self.face_id = face_id

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

    def move_to(
        self, new_position: tuple[int], ori: Orientation = None, face_id: int = None
    ) -> None:
        """Change position of the explorer."""
        self.row, self.col = new_position
        if face_id:
            self.face_id = face_id
        if ori:
            self.ori = ori

    def get_password(self, mapping_global: tuple[int]) -> int:
        """The final password is the sum of 1000 times the row, 4 times the column, and the facing."""
        row = self.row + mapping_global[0]
        col = self.col + mapping_global[1]
        return 1000 * (row + 1) + 4 * (col + 1) + self.DIRECTION_PASSW[self.ori]


class DiceFace:
    """
    boundary_data = {
        xxx_face: {
            id: int,
            ori: Orientation
            },
        ...
        }
    xxx = top, right, down or left
    """

    def __init__(
        self,
        dimension: int,
        id: int,
        wall_tiles: list[tuple[int]],
        global_corner_coordinates: tuple[int],
        boundary_data: dict,
    ) -> None:
        self.id = id
        self.board = np.zeros((dimension, dimension))
        self.max_val = dimension - 1
        self.global_corner_coordinate = global_corner_coordinates
        self._add_walls(wall_tiles)
        self.boundaries = boundary_data

    def _add_walls(self, wall_tiles: list[tuple[int]]) -> None:
        for coordinate in wall_tiles:
            self.board[coordinate] = 1


class CubeMap:

    ROTATION_DIR = [
        Orientation.RIGTH,
        Orientation.DOWN,
        Orientation.LEFT,
        Orientation.TOP,
        Orientation.RIGTH,
        Orientation.TOP,
    ]

    def __init__(self, faces: list[DiceFace]) -> None:
        self.faces = faces
        # Position Explorer
        self.explorer = self._position_explorer()

    def _position_explorer(self) -> Explorer:
        """You begin the path in the face with id 1 at the leftmost open tile of the top row of tiles."""
        # Default values
        initial_row = 0
        initial_face = 1
        ori = Orientation.RIGTH
        # Calculate column initial value
        face = self.faces[initial_face - 1]
        for col, val in enumerate(face.board[initial_row]):
            if val == 0:
                y = col
                break
        return Explorer(initial_row, y, ori, initial_face)

    def _find_opposite_position(self, current_position: tuple[int]) -> tuple[int]:
        # Input data
        row, col = current_position
        face = self.faces[self.explorer.face_id - 1]
        current_ori = self.explorer.ori
        # Calculate next ori and next face id
        if current_ori == Orientation.RIGTH:
            boundary = face.boundaries["right_face"]
        elif current_ori == Orientation.DOWN:
            boundary = face.boundaries["down_face"]
        elif current_ori == Orientation.LEFT:
            boundary = face.boundaries["left_face"]
        elif current_ori == Orientation.TOP:
            boundary = face.boundaries["top_face"]
        next_ori = boundary["ori"]
        next_face_id = boundary["id"]
        # Calculate position in next face
        max_i = face.max_val
        if current_ori == Orientation.RIGTH:
            if next_ori == Orientation.RIGTH:
                next_position = (row, 0)
            elif next_ori == Orientation.DOWN:
                next_position = (0, max_i - row)
            elif next_ori == Orientation.LEFT:
                next_position = (max_i - row, max_i)
            elif next_ori == Orientation.TOP:
                next_position = (max_i, row)
        elif current_ori == Orientation.DOWN:
            if next_ori == Orientation.RIGTH:
                next_position = (max_i - col, 0)
            elif next_ori == Orientation.DOWN:
                next_position = (0, col)
            elif next_ori == Orientation.LEFT:
                next_position = (col, max_i)
            elif next_ori == Orientation.TOP:
                next_position = (max_i, max_i - col)
        elif current_ori == Orientation.LEFT:
            if next_ori == Orientation.RIGTH:
                next_position = (max_i - row, 0)
            elif next_ori == Orientation.DOWN:
                next_position = (0, row)
            elif next_ori == Orientation.LEFT:
                next_position = (row, max_i)
            elif next_ori == Orientation.TOP:
                next_position = (max_i, max_i - row)
        elif current_ori == Orientation.TOP:
            if next_ori == Orientation.RIGTH:
                next_position = (col, 0)
            elif next_ori == Orientation.DOWN:
                next_position = (0, max_i - col)
            elif next_ori == Orientation.LEFT:
                next_position = (max_i - col, max_i)
            elif next_ori == Orientation.TOP:
                next_position = (max_i, col)

        return next_position, next_ori, next_face_id

    def follow_directions(self, directions: list[int | str]) -> None:
        for direction in directions:
            if isinstance(direction, int):
                # Move forward until rock
                for _ in range(direction):
                    next_position = self.explorer.get_next_position()
                    try:
                        if next_position[0] < 0 or next_position[1] < 0:
                            raise IndexError
                        # Check it is not a rock and move
                        board = self.faces[self.explorer.face_id - 1].board
                        if board[next_position] == 1:
                            break
                        else:
                            self.explorer.move_to(next_position)
                    except IndexError:
                        # Outside of the board
                        (
                            next_position,
                            next_ori,
                            next_face_id,
                        ) = self._find_opposite_position(
                            (self.explorer.row, self.explorer.col)
                        )
                        # Check it is not a rock and move
                        board = self.faces[next_face_id - 1].board

                        if board[next_position] == 1:
                            break
                        else:
                            self.explorer.move_to(next_position, next_ori, next_face_id)
            else:
                # Change facing direction
                if direction == "R":
                    new_ori = self.ROTATION_DIR[
                        self.ROTATION_DIR.index(self.explorer.ori) + 1
                    ]
                elif direction == "L":
                    new_ori = self.ROTATION_DIR[
                        self.ROTATION_DIR.index(self.explorer.ori) - 1
                    ]
                self.explorer.ori = new_ori

    def get_password(self) -> int:
        face = self.faces[self.explorer.face_id - 1]
        global_mapping = face.global_corner_coordinate
        return self.explorer.get_password(global_mapping)


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


def create_wall_tiles_for_each_face(
    raw_map: list[str], face_size: int
) -> list[list[tuple[int]]]:
    """Parse raw map and returns a list with 6 list with the wall relative coordinates"""
    faces_walls = list()
    coordinates_corners_faces = list()
    first_r_face_id = 0
    for row, line in enumerate(raw_map):
        quotient_r, mod_r = divmod(row, face_size)
        if mod_r == 0:
            faces_in_row = len(line) // face_size
            for _ in range(faces_in_row):
                faces_walls.append(list())
            if quotient_r != 0:
                first_r_face_id = face_num + 1
        for col, char in enumerate(line):
            quotient_c, mod_c = divmod(col, face_size)
            if mod_c == 0:
                face_num = first_r_face_id + quotient_c
                if mod_r == 0:
                    coordinates_corners_faces.append((row, col))
            if char == "#":
                wall_tiles = faces_walls[face_num]
                wall_tiles.append((row % face_size, col % face_size))
    # Store only faces from dice and corner coordinates of each face
    faces_w = list()
    global_corner_coords = list()
    for face, global_coordinate in zip(faces_walls, coordinates_corners_faces):
        if face:
            faces_w.append(face)
            global_corner_coords.append(global_coordinate)
    return faces_w, global_corner_coords


def main():
    # Input data needed
    # face_size = 4  # test_input.txt
    # boundary_data = {
    #     "1": {
    #         "top_face": {"id": 2, "ori": Orientation.DOWN},
    #         "right_face": {"id": 6, "ori": Orientation.LEFT},
    #         "down_face": {"id": 4, "ori": Orientation.DOWN},
    #         "left_face": {"id": 3, "ori": Orientation.DOWN},
    #     },
    #     "2": {
    #         "top_face": {"id": 1, "ori": Orientation.DOWN},
    #         "right_face": {"id": 3, "ori": Orientation.RIGTH},
    #         "down_face": {"id": 5, "ori": Orientation.TOP},
    #         "left_face": {"id": 6, "ori": Orientation.TOP},
    #     },
    #     "3": {
    #         "top_face": {"id": 1, "ori": Orientation.RIGTH},
    #         "right_face": {"id": 4, "ori": Orientation.RIGTH},
    #         "down_face": {"id": 5, "ori": Orientation.RIGTH},
    #         "left_face": {"id": 2, "ori": Orientation.LEFT},
    #     },
    #     "4": {
    #         "top_face": {"id": 1, "ori": Orientation.TOP},
    #         "right_face": {"id": 6, "ori": Orientation.DOWN},
    #         "down_face": {"id": 5, "ori": Orientation.DOWN},
    #         "left_face": {"id": 3, "ori": Orientation.LEFT},
    #     },
    #     "5": {
    #         "top_face": {"id": 4, "ori": Orientation.TOP},
    #         "right_face": {"id": 6, "ori": Orientation.RIGTH},
    #         "down_face": {"id": 2, "ori": Orientation.TOP},
    #         "left_face": {"id": 3, "ori": Orientation.TOP},
    #     },
    #     "6": {
    #         "top_face": {"id": 4, "ori": Orientation.LEFT},
    #         "right_face": {"id": 1, "ori": Orientation.LEFT},
    #         "down_face": {"id": 2, "ori": Orientation.RIGTH},
    #         "left_face": {"id": 5, "ori": Orientation.LEFT},
    #     },
    # }
    face_size = 50  # input.txt
    boundary_data = {
        "1": {
            "top_face": {"id": 6, "ori": Orientation.LEFT},
            "right_face": {"id": 2, "ori": Orientation.RIGTH},
            "down_face": {"id": 3, "ori": Orientation.DOWN},
            "left_face": {"id": 4, "ori": Orientation.RIGTH},
        },
        "2": {
            "top_face": {"id": 6, "ori": Orientation.TOP},
            "right_face": {"id": 5, "ori": Orientation.LEFT},
            "down_face": {"id": 3, "ori": Orientation.LEFT},
            "left_face": {"id": 1, "ori": Orientation.LEFT},
        },
        "3": {
            "top_face": {"id": 1, "ori": Orientation.TOP},
            "right_face": {"id": 2, "ori": Orientation.TOP},
            "down_face": {"id": 5, "ori": Orientation.DOWN},
            "left_face": {"id": 4, "ori": Orientation.DOWN},
        },
        "4": {
            "top_face": {"id": 3, "ori": Orientation.RIGTH},
            "right_face": {"id": 5, "ori": Orientation.RIGTH},
            "down_face": {"id": 6, "ori": Orientation.DOWN},
            "left_face": {"id": 1, "ori": Orientation.RIGTH},
        },
        "5": {
            "top_face": {"id": 3, "ori": Orientation.TOP},
            "right_face": {"id": 2, "ori": Orientation.LEFT},
            "down_face": {"id": 6, "ori": Orientation.RIGTH},
            "left_face": {"id": 4, "ori": Orientation.LEFT},
        },
        "6": {
            "top_face": {"id": 4, "ori": Orientation.TOP},
            "right_face": {"id": 1, "ori": Orientation.DOWN},
            "down_face": {"id": 2, "ori": Orientation.DOWN},
            "left_face": {"id": 5, "ori": Orientation.TOP},
        },
    }
    # Read file data
    raw_map, raw_directions = parse_input(INPUT_FILE)
    directions = parse_directions(raw_directions)
    walls_tiles, corner_face_coords = create_wall_tiles_for_each_face(
        raw_map, face_size
    )
    # Create DiceFace
    face_boards = list()
    for i, wall_tiles in enumerate(walls_tiles):
        face_id = i + 1
        face = DiceFace(
            face_size,
            face_id,
            wall_tiles,
            corner_face_coords[i],
            boundary_data[f"{face_id}"],
        )
        face_boards.append(face)
    # Create cub map and follow directions
    password_map = CubeMap(face_boards)
    password_map.follow_directions(directions)
    # Get the password
    part_2 = password_map.get_password()
    print(part_2)

    explorer = password_map.explorer
    print(f"Explorer is in dice face: {explorer.face_id}")
    print(f"At coordinates: ({explorer.row}, {explorer.col})")


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"--- {(time.time() - start) * 1000} ms ---")
