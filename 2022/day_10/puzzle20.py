from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

INPUT_FILE = Path(__file__).parent / "input.txt"
# INPUT_FILE = Path(__file__).parent / "test_input.txt"
# INPUT_FILE = Path(__file__).parent / "large_test_input.txt"


class Clockcircuit:
    def __init__(self) -> None:
        self.cycle = 1
        self.register = 1
        self.crt = CRT()

    def noop(self) -> None:
        self.crt.check_sprite(self.cycle, self.register)
        self.cycle += 1

    def addx(self, v: int) -> None:
        self.crt.check_sprite(self.cycle, self.register)
        self.cycle += 1
        self.crt.check_sprite(self.cycle, self.register)
        self.cycle += 1
        self.register += v


class CRT:
    WIDE = 40
    HEIGH = 6

    def __init__(self) -> None:
        self.screen = np.zeros((self.HEIGH, self.WIDE))

    def _current_screen_position(self, cycle: int) -> tuple[int]:
        """returns row and column in screen"""
        return divmod(cycle - 1, 40)

    def _sprite_visible(self, pixel: int, register: int) -> bool:
        return pixel >= register - 1 and pixel <= register + 1

    def check_sprite(self, cycle: int, register: int) -> None:
        screen_pos = self._current_screen_position(cycle)
        pixel = screen_pos[1]
        if self._sprite_visible(pixel, register):
            self.screen[screen_pos] = 1

    def render(self) -> int:
        plt.imshow(self.screen)
        plt.show()


def main() -> None:
    clock = Clockcircuit()
    with open(INPUT_FILE, "r") as file:
        for line in file:
            command, *v = line.split()
            if command == "noop":
                clock.noop()
            elif command == "addx":
                clock.addx(int(v[0]))
    clock.crt.render()


if __name__ == "__main__":
    main()
