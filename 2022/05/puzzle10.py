from pathlib import Path
import re

INPUT_FILE = Path(__file__).parent / "input.txt"
COL = 4


class CargoStacks:
    def __init__(self, crates: list[list[str]]) -> None:
        self.cargo_lines = {
            "1": list(),
            "2": list(),
            "3": list(),
            "4": list(),
            "5": list(),
            "6": list(),
            "7": list(),
            "8": list(),
            "9": list(),
        }
        self._fill_cargo_lines(crates)

    def move_crates(self, number: int, ini_stack: str, end_stack: str) -> None:
        removed_cargo = [self.cargo_lines[ini_stack].pop() for _ in range(number)]
        removed_cargo.reverse()
        self.cargo_lines[end_stack].extend(removed_cargo)

    def give_last_creates(self) -> str:
        last_crates = [stack[-1] for stack in self.cargo_lines.values()]
        return "".join(last_crates)

    def _fill_cargo_lines(self, crates: list[list[str]]) -> None:
        while crates:
            cargo_level = crates.pop()
            for i, cargo in enumerate(cargo_level):
                crate = re.search("[A-Z]", cargo)
                if crate:
                    crate_letter = crate.group()
                    self.cargo_lines[str(i + 1)].append(crate_letter)

    def __str__(self) -> str:
        stack_1 = self.cargo_lines["1"]
        stack_2 = self.cargo_lines["2"]
        stack_3 = self.cargo_lines["3"]
        stack_4 = self.cargo_lines["4"]
        stack_5 = self.cargo_lines["5"]
        stack_6 = self.cargo_lines["6"]
        stack_7 = self.cargo_lines["7"]
        stack_8 = self.cargo_lines["8"]
        stack_9 = self.cargo_lines["9"]
        display = f"1: {stack_1}\n2: {stack_2}\n3: {stack_3}\n4: {stack_4}\n5: {stack_5}\n6: {stack_6}\n7: {stack_7}\n8: {stack_8}\n 9: {stack_9}"
        return display


def split_by_columns(line: str) -> list[str]:
    return [line[i : i + COL] for i in range(0, len(line), COL)]


def parse_operation(line: str) -> tuple[str]:
    pattern_text = r"\w+\s+(\d+)\s+\w+\s+(\d+)\s+\w+\s+(\d+)"
    pattern = re.compile(pattern_text)
    match = pattern.match(line)
    return match.groups()


def main() -> None:
    with open(INPUT_FILE, "r") as file:
        reading_crates = True
        cargo_levels = list()
        for line in file:
            # Initial parsing of the crates info
            if reading_crates:
                level_cargo = split_by_columns(line)
                try:
                    number = int(level_cargo[0])
                except ValueError:
                    cargo_levels.append(level_cargo)
                else:
                    skip_line = next(file)
                    reading_crates = False
                    # Prepare crates stacks
                    port = CargoStacks(cargo_levels)

            # Stack operations
            else:
                num, ori, dst = parse_operation(line)
                port.move_crates(int(num), ori, dst)
                a = 2

    print(port)
    print(port.give_last_creates())


if __name__ == "__main__":
    main()
