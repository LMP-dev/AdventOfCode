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
    Direction.RIGHT: (0, 1),
    Direction.UP: (-1, 0),
    Direction.LEFT: (0, -1),
    Direction.DOWN: (1, 0),
}


@dataclass
class CityBlock:
    loc: tuple[int, int]
    coming_from: Direction
    accumulated_heat_loss: int
    last_three_moves: list[Direction] = field(default_factory=list)
    heat_loss_path: list[int] = field(default_factory=list)

    def next_blocks(self, grid: dict[tuple[int, int], int]) -> list[CityBlock]:
        next_allowed_blocks = []

        # Find allowed new directions
        next_directions: list[Direction] = [
            Direction.RIGHT,
            Direction.UP,
            Direction.LEFT,
            Direction.DOWN,
        ]
        try:
            next_directions.remove(OPPOSITE_DIRECTION[self.coming_from])
        except ValueError:
            pass

        # Avoid moving more than 3 consequtive directions
        if self.check_three_same_last_moves():
            next_directions.remove(self.last_three_moves[0])

        for direction in next_directions:
            next_loc = self._next_location(direction)
            if next_loc not in grid:
                continue
            next_allowed_blocks.append(
                self._create_new_block(next_loc, direction, grid[next_loc])
            )

        return next_allowed_blocks

    def update_last_moves(self, last_direction: Direction) -> None:
        if len(self.last_three_moves) == 3:
            self.last_three_moves.pop(0)
            self.last_three_moves.append(last_direction)
        else:
            self.last_three_moves.append(last_direction)

    def check_three_same_last_moves(self) -> bool:
        if self.last_three_moves:
            if self.last_three_moves.count(self.last_three_moves[0]) == 3:
                return True

    def _next_location(self, direction: Direction) -> tuple[int, int]:
        offset = NEXT_STEP_OFFSETS[direction]
        return add_tuples(self.loc, offset)

    def _create_new_block(
        self, loc: tuple[int, int], coming_from: Direction, heat_loss: int
    ) -> CityBlock:
        block = CityBlock(loc, coming_from, self.accumulated_heat_loss + heat_loss)
        block.heat_loss_path = self.heat_loss_path.copy()
        block.last_three_moves = self.last_three_moves.copy()
        block.heat_loss_path.append(heat_loss)
        block.update_last_moves(coming_from)
        return block


def add_tuples(one: tuple[int, int], other: tuple[int, int]) -> tuple[int, int]:
    return (one[0] + other[0], one[1] + other[1])
