# Standard library
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto


class Direction(Enum):
    RIGHT = auto()
    UP = auto()
    LEFT = auto()
    DOWN = auto()


OPPOSITE_DIRECTION = {
    Direction.RIGHT: Direction.LEFT,
    Direction.UP: Direction.DOWN,
    Direction.LEFT: Direction.RIGHT,
    Direction.DOWN: Direction.UP,
}

NEXT_STEP_OFFSETS: dict[Direction, tuple[int, int]] = {
    Direction.RIGTH: (0, 1),
    Direction.UP: (-1, 0),
    Direction.LEFT: (0, -1),
    Direction.DOWN: (1, 0),
}


def add_tuples(one: tuple[int, int], other: tuple[int, int]) -> tuple[int, int]:
    return (one[0] + other[0], one[1] + other[1])


@dataclass
class CityBlock:
    loc: tuple[int, int]
    coming_from: Direction
    heat_loss: int
    last_three_moves: list[Direction] = field(default_factory=list)
    heat_loss_path: list[int] = field(default_factory=list)

    def next_blocks(self, grid: Grid) -> list[CityBlock]:
        next_allowed_blocks = []

        # Find allowed new directions
        next_directions: list[Direction] = Direction._member_names_.remove(
            OPPOSITE_DIRECTION[self.coming_from]
        )
        # Avoid moving more than 3 consequtive directions
        if self.last_three_moves.count(self.last_three_moves[0]) == 3:
            try:
                next_directions.remove(self.last_three_moves[0])
            except ValueError:
                pass

        for direction in next_directions:


        return

    def update_last_moves(self, last_direction: Direction) -> None:
        self.last_three_moves.pop(0)
        self.last_three_moves.append(last_direction)

    def _create_new_block(
        self, loc: tuple[int, int], coming_from: Direction, heat_loss: int
    ) -> CityBlock:
        block = CityBlock(loc, coming_from, heat_loss)
        block.heat_loss_path.append(heat_loss)
        block.update_last_moves(coming_from)
        return block
