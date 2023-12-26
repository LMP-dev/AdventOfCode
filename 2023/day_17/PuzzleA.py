# Standard library
from pathlib import Path

# .py modules
from city_block import CityBlock, Direction
import distance

INPUT_FILE_PATH = Path(__file__).parent


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


Grid = dict[tuple[int, int], int]


def parse_input(file_content: list[str]) -> Grid:
    grid = dict()
    for r, line in enumerate(file_content):
        # Parse lines and add extra expanded rows when all "."
        row = list(line)
        grid.update({(r, c): char for c, char in enumerate(row)})
    return grid


def solve_01(data) -> int:
    queue: list[CityBlock] = [CityBlock((0, 0), Direction.RIGHT, data[(0, 0)])]
    visited: list[tuple(int, int)] = []

    finishing_loc = max(data.keys())
    distance_funct = distance.get_distance_a_star(finishing_loc)

    while queue:
        # Sort according to heat loss
        queue.sort(key=distance.distance_dikstra)
        current_block = queue.pop(0)

        if current_block.loc in visited:
            continue
        visited.append(current_block.loc)

        if current_block.loc == finishing_loc:
            break
        else:
            queue.extend(current_block.next_blocks(data))

    return sum(current_block.heat_loss_path)


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the example 1 is {solution}")
    # file_content = read_data(INPUT_FILE_PATH / "input.txt")
    # data = parse_input(file_content)
    # solution = solve_01(data)
    # print(f"The solution of the part 1 is {solution}")


if __name__ == "__main__":
    main()
