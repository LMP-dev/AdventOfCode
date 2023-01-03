from pathlib import Path
import time
from collections import deque
from enum import Enum, auto

INPUT_FILE = Path(__file__).parent / "input.txt"
# INPUT_FILE = Path(__file__).parent / "test_input.txt"  # sol = 110


class Movement(Enum):
    N = auto()
    S = auto()
    W = auto()
    E = auto()


class Elf:
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
        self.next_position = None

    @property
    def N(self) -> tuple[int]:
        return (self.row - 1, self.col)  # N

    @property
    def S(self) -> tuple[int]:
        return (self.row + 1, self.col)  # S

    @property
    def W(self) -> tuple[int]:
        return (self.row, self.col - 1)  # W

    @property
    def E(self) -> tuple[int]:
        return (self.row, self.col + 1)  # E

    @property
    def NW(self) -> tuple[int]:
        return (self.row - 1, self.col - 1)  # NW

    @property
    def NE(self) -> tuple[int]:
        return (self.row - 1, self.col + 1)  # NE

    @property
    def SW(self) -> tuple[int]:
        return (self.row + 1, self.col - 1)  # SW

    @property
    def SE(self) -> tuple[int]:
        return (self.row + 1, self.col + 1)  # SE

    def get_8_around_positions(self) -> set[tuple[int]]:
        around_pos = [
            self.NW,
            self.N,
            self.NE,
            self.W,
            self.E,
            self.SW,
            self.S,
            self.SE,
        ]
        return set(around_pos)

    def get_positions_in_direction(self, direction: Movement) -> set[tuple[int]]:
        if direction == Movement.N:
            pos_direction = [self.NW, self.N, self.NE]
        elif direction == Movement.S:
            pos_direction = [self.SW, self.S, self.SE]
        elif direction == Movement.W:
            pos_direction = [self.NW, self.W, self.SW]
        elif direction == Movement.E:
            pos_direction = [self.NE, self.E, self.SE]
        return set(pos_direction)

    def update_next_position(self, direction: Movement):
        if direction == Movement.N:
            self._set_next_position(self.N)
        elif direction == Movement.S:
            self._set_next_position(self.S)
        elif direction == Movement.W:
            self._set_next_position(self.W)
        elif direction == Movement.E:
            self._set_next_position(self.E)

    def _set_next_position(self, position: tuple[int]) -> None:
        self.next_position = position

    def move_to_next_position(self) -> None:
        self.row, self.col = self.next_position
        self.next_position = None

    def reset_next_position(self) -> None:
        self.next_position = None


class MovingProcess:
    """
        N
     NW   NE
    W   +   E
     SW   SE
        S
    No elves around (8 directions) -> DO nothing
    Look 4 directiona:
        no elf in N, NE, NW -> move N
        no elf in S, SE, SW -> move S
        no elf in W, NW, SW -> move W
        no elf in E, NE, SE -> move E
    """

    MOVEMENT = deque([Movement.N, Movement.S, Movement.W, Movement.E])

    def __init__(self, elves_positions: set[tuple[int]]) -> None:
        self.elves = [Elf(r, c) for r, c in elves_positions]
        self.current_positions = elves_positions

    def _round_first_half(self) -> set[tuple[int]]:
        """Elves considers next movement"""
        movement_list = set()
        banned_moves = set()
        for elf in self.elves:
            # Checks 8 positions are free
            around_elf_pos = elf.get_8_around_positions()
            if around_elf_pos & self.current_positions:
                # Decide next movement
                for move in self.MOVEMENT:
                    positions = elf.get_positions_in_direction(move)
                    if not positions & self.current_positions:
                        elf.update_next_position(move)
                        if elf.next_position in movement_list:
                            banned_moves.add(elf.next_position)
                        else:
                            movement_list.add(elf.next_position)
                        break
        return banned_moves

    def _round_second_half(self, banned_moves: set[tuple[int]]) -> None:
        """Elves moves if they can"""
        for elf in self.elves:
            if elf.next_position:
                if elf.next_position in banned_moves:
                    elf.reset_next_position()
                else:
                    elf.move_to_next_position()

    def _update_current_positions(self) -> None:
        self.current_positions = set([(elf.row, elf.col) for elf in self.elves])

    def run_round(self) -> None:
        banned_moves = self._round_first_half()
        self._round_second_half(banned_moves)
        self._update_current_positions()
        self.update_movement()

    def update_movement(self) -> None:
        self.MOVEMENT.append(self.MOVEMENT.popleft())


def parse_input(file_path: Path) -> set[tuple[int]]:
    """Caculate original coordinates for elf position"""
    elves_positions = set()
    with open(file_path, "r") as file:
        for row, line in enumerate(file):
            for col, char in enumerate(line):
                if char == "#":
                    elves_positions.add((row, col))
    return elves_positions


def main():
    elves_positions = parse_input(INPUT_FILE)
    moving_process = MovingProcess(elves_positions)
    for _ in range(10):
        moving_process.run_round()
    min_row = float("inf")
    min_col = float("inf")
    max_row = float("-inf")
    max_col = float("-inf")
    for elf in moving_process.elves:
        if min_row > elf.row:
            min_row = elf.row
        if max_row < elf.row:
            max_row = elf.row
        if min_col > elf.col:
            min_col = elf.col
        if max_col < elf.col:
            max_col = elf.col
    side_a = max_row - min_row + 1
    side_b = max_col - min_col + 1
    part_1 = side_a * side_b - len(elves_positions)
    print(part_1)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"--- {(time.time() - start) * 1000} ms ---")
