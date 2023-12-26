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
        grid.update({(r, c): int(value) for c, value in enumerate(row)})
    return grid


def solve_01(data) -> int:
    queue: list[CityBlock] = [CityBlock((0, 0), Direction.DOWN, 0)]
    visited: set[tuple(int, int)] = set()

    finishing_loc = max(data.keys())
    # distance_funct = distance.get_distance_a_star(finishing_loc)

    while queue:
        # Sort according to heat loss
        queue.sort(key=distance.distance_dikstra)

        lowest_block = queue.pop(0)
        # try:
        #     if lowest_block.accumulated_heat_loss == queue[0].accumulated_heat_loss:
        #         print(
        #             f"There was more blocks with same min distance!!!\nBlock: {lowest_block} and {queue[0]}"
        #         )
        # except IndexError:
        #     pass

        if lowest_block.loc in visited:
            continue
        visited.add(lowest_block.loc)

        if lowest_block.loc == finishing_loc:
            break
        else:
            queue.extend(lowest_block.next_blocks(data))

    print(lowest_block.heat_loss_path)
    return lowest_block.accumulated_heat_loss


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
