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
        self.crt = CRT(self)

    def noop(self) -> None:
        self.crt.check_sprite()
        self.cycle += 1

    def addx(self, v: int) -> None:
        self.crt.check_sprite()
        self.cycle += 1
        self.crt.check_sprite()
        self.cycle += 1
        self.register += v


class CRT:
    WIDE = 40
    HEIGH = 6

    def __init__(self, clock_circuit: Clockcircuit) -> None:
        self.cpu = clock_circuit
        self.screen = np.zeros((self.HEIGH, self.WIDE))

    def _current_screen_position(self) -> tuple[int]:
        """returns row and column in screen"""
        return divmod(self.cpu.cycle - 1, 40)

    def _sprite_visible(self, pixel: int, register: int) -> bool:
        return pixel >= register - 1 and pixel <= register + 1

    def check_sprite(self) -> None:
        screen_pos = self._current_screen_position()
        pixel = screen_pos[1]
        if self._sprite_visible(pixel, self.cpu.register):
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
