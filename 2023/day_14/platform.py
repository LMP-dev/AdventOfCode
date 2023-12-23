from dataclasses import dataclass
from enum import Enum, auto

import operations

coord = tuple[int, int]


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

    def __post__init__(self) -> None:
        # Ensure the lists in schema are ordered in ascending order!
        ...


@dataclass
class Platform:
    round_rocks: list[coord]
    cube_rocks: list[coord]
    max_row: int
    max_col: int

    def organize_rocks_by_column(self) -> PlatformByLines:
        platform = {}
        for col in range(self.max_col + 1):
            platform.update({col: {Shape.ROUND: [], Shape.CUBE: []}})
        for rock in self.round_rocks:
            r, c = rock
            platform[c][Shape.ROUND].append(r)
        for rock in self.cube_rocks:
            r, c = rock
            platform[c][Shape.CUBE].append(r)
        return PlatformByLines(Orientation.COLUMNS, platform)

    def organize_rocks_by_row(self) -> PlatformByLines:
        platform = {}
        for row in range(self.max_row + 1):
            platform.update({row: {Shape.ROUND: [], Shape.CUBE: []}})
        for rock in self.round_rocks:
            r, c = rock
            platform[r][Shape.ROUND].append(c)
        for rock in self.cube_rocks:
            r, c = rock
            platform[r][Shape.CUBE].append(c)
        return PlatformByLines(Orientation.ROWS, platform)

    def update_round_rocks(self, new_round_rocks: list[coord]) -> None:
        self.round_rocks = new_round_rocks
