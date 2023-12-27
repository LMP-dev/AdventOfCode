# Standard library
from pathlib import Path
from dataclasses import dataclass

INPUT_FILE_PATH = Path(__file__).parent


MOVEMENT: dict[str, tuple[int, int]] = {
    "R": (0, 1),
    "U": (-1, 0),
    "L": (0, -1),
    "D": (1, 0),
}


@dataclass
class Trench:
    position: tuple[int, int]
    color: str


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> list[tuple[str, int, str]]:
    instructions = []
    for line in file_content:
        dir, steps, color = line.split(" ")
        instructions.append((dir, int(steps), color[1:-1]))
    return instructions


def add_tuples(one: tuple[int, int], other: tuple[int, int]) -> tuple[int, int]:
    return (one[0] + other[0], one[1] + other[1])


def dig_trenches(
    current_pos: tuple[int, int], direction: str, steps: int, color: str
) -> tuple[list[Trench], tuple[int, int]]:
    trenches = []
    offset = MOVEMENT[direction]
    for _ in range(steps):
        current_pos = add_tuples(current_pos, offset)
        trenches.append(Trench(current_pos, color))
    return trenches, current_pos


def dig_inside_trenches_loop(trenches: list[Trench]) -> list[tuple[int, int]]:
    ...


def solve_01(data: list[tuple[str, int, str]]) -> int:
    current_pos = (0, 0)
    loop_trenches: list[Trench] = []

    # Dig loop trenches
    for instruction in data:
        direction, steps, color = instruction
        new_trenches, current_pos = dig_trenches(current_pos, direction, steps, color)
        loop_trenches.extend(new_trenches)

    # Dig inside loop
    inside_holes = dig_inside_trenches_loop(loop_trenches)

    return len(loop_trenches)  # + len(inside_holes)


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the example 1 is {solution}")
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the part 1 is {solution}")


if __name__ == "__main__":
    main()
