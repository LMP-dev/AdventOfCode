from dataclasses import dataclass
from enum import Enum, auto

coord = tuple[int,int]

class Shape(Enum):
    ROUND = auto()
    CUBE = auto()

class Orientation(Enum):
    ROWS = auto()
    COLUMNS = auto()


@dataclass
class PlatformByLines:
    orientation: Orientation
    schema: dict[int, dict[str, list[int]]]


@dataclass
class Platform:
    round_rocks: list[coord]
    cube_rocks: list[coord]
    max_row: int
    max_col:int

    def organize_rocks_by_column(self):
        ...