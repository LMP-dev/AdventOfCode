# Standard library
import itertools
import math
from pathlib import Path

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


def find_nodes_ends_A(network: dict[str, tuple[str, str]]) -> tuple[str]:
    start_paths = []
    for node in network.keys():
        if node[2] == "A":
            start_paths.append(node)
    return tuple(start_paths)


def navigate_desert(
    network: dict[str, tuple[str, str]], current_node: str, direction: str
) -> str:
    """Use the network defined above to be able to cache the function"""
    if direction == "L":
        next_node = network[current_node][0]
    elif direction == "R":
        next_node = network[current_node][1]
    else:
        raise Exception(f"Unknownn instruction: {direction}")
    return next_node


def solve_02(data: tuple[str, dict[str, tuple[str, str]]]) -> int:
    steps = 0
    path_steps = []

    instructions = itertools.cycle(data[0])
    network = data[1]
    current_nodes = find_nodes_ends_A(network)

    while len(current_nodes) > 0:
        next_path = next(instructions)
        steps += 1

        next_nodes = []
        for node in current_nodes:
            next_node = navigate_desert(network, node, next_path)
            if next_node[2] == "Z":
                path_steps.append(steps)
            else:
                next_nodes.append(next_node)
        current_nodes = next_nodes

    return math.lcm(*path_steps)


def main() -> None:
    # input.txt | example_1.txt | example_1_v2.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the example 1 is {solution}")
    file_content = read_data(INPUT_FILE_PATH / "example_1_v2.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the example 1 v2 is {solution}")
    file_content = read_data(INPUT_FILE_PATH / "example_2.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the example 2 is {solution}")
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the part 2 is {solution}")


if __name__ == "__main__":
    main()
