from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto


coord = tuple[int, int]


class Shape(Enum):
    ROUND = auto()
    CUBE = auto()


@dataclass
class Platform:
    round_rocks: list[coord]
    cube_rocks: list[coord]
    max_row: int
    max_col: int

    def organize_rocks_by_column(self) -> dict[int, dict[str, list[int]]]:
        platform = {}
        for col in range(self.max_col + 1):
            platform.update({col: {Shape.ROUND: [], Shape.CUBE: []}})
        for rock in self.round_rocks:
            r, c = rock
            platform[c][Shape.ROUND].append(r)
        for rock in self.cube_rocks:
            r, c = rock
            platform[c][Shape.CUBE].append(r)
        return platform

    def organize_rocks_by_row(self) -> dict[int, dict[str, list[int]]]:
        platform = {}
        for row in range(self.max_row + 1):
            platform.update({row: {Shape.ROUND: [], Shape.CUBE: []}})
        for rock in self.round_rocks:
            r, c = rock
            platform[r][Shape.ROUND].append(c)
        for rock in self.cube_rocks:
            r, c = rock
            platform[r][Shape.CUBE].append(c)
        return platform

    def update_round_rocks(self, new_round_rocks: list[coord]) -> None:
        self.round_rocks = new_round_rocks

    def get_copy_object(self) -> Platform:
        return Platform(self.round_rocks, self.cube_rocks, self.max_row, self.max_col)

    def get_rock_rows(self) -> list[int]:
        return [r for (r, c) in self.round_rocks]
