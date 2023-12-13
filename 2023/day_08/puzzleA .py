# Standard library
from pathlib import Path
import itertools

INPUT_FILE_PATH = Path(__file__).parent


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> tuple[str, dict[str, tuple[str, str]]]:
    instructions = file_content[0]
    network = {}

    for node_data in file_content[2:]:
        node = node_data[:3]
        left_coord = node_data[7:10]
        right_coord = node_data[12:15]
        network.update({node: (left_coord, right_coord)})
    return instructions, network


def solve_01(data: tuple[str, dict[str, tuple[str, str]]]) -> int:
    steps = 0

    instructions = itertools.cycle(data[0])
    network = data[1]
    current_node = "AAA"

    for next_path in instructions:
        steps += 1
        if next_path == "L":
            next_node = network[current_node][0]
        elif next_path == "R":
            next_node = network[current_node][1]
        else:
            raise Exception(f"Unknownn instruction: {next_path}")
        if next_node == "ZZZ":
            break
        else:
            current_node = next_node

    return steps


def main() -> None:
    # input.txt | example_1.txt | example_1_v2.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the example 1 is {solution}")
    file_content = read_data(INPUT_FILE_PATH / "example_1_v2.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the example 1 v2 is {solution}")
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the part 1 is {solution}")


if __name__ == "__main__":
    main()
