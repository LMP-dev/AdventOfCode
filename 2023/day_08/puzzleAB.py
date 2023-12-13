# Standard library
from pathlib import Path
import itertools
from typing import Iterable
from functools import cache, partial

INPUT_FILE_PATH = Path(__file__).parent


class HashableDict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> tuple[str, dict[str, tuple[str, str]]]:
    instructions = file_content[0]
    network = HashableDict()

    for node_data in file_content[2:]:
        node = node_data[:3]
        left_coord = node_data[7:10]
        right_coord = node_data[12:15]
        network.update({node: (left_coord, right_coord)})
    return instructions, network


def find_nodes_ends_A(network: HashableDict) -> tuple[str]:
    start_paths = []
    for node in network.keys():
        if node[2] == "A":
            start_paths.append(node)
    return tuple(start_paths)


def is_final_destination(nodes: Iterable[str]) -> bool:
    for node in nodes:
        if node[2] != "Z":
            return False
    return True


@cache
def navigate_desert(network: HashableDict, current_node: str, direction: str) -> str:
    if direction == "L":
        node = network[current_node][0]
    elif direction == "R":
        node = network[current_node][0]
    else:
        raise Exception(f"Unknownn instruction: {direction}")
    return node


def solve_01(data: tuple[str, HashableDict]) -> int:
    steps = 0

    instructions = itertools.cycle(data[0])
    network = data[1]
    current_nodes = tuple(find_nodes_ends_A(network))

    for next_path in instructions:
        steps += 1
        next_nodes = []
        for node in current_nodes:
            next_node = navigate_desert(network, node, next_path)
            next_nodes.append(next_node)
        if is_final_destination(next_nodes):
            break
        else:
            current_nodes = tuple(next_nodes)

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
    file_content = read_data(INPUT_FILE_PATH / "example_2.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the example 2 is {solution}")
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the part 2 is {solution}")


if __name__ == "__main__":
    main()
