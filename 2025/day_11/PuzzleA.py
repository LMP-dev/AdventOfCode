# Standard library
from pathlib import Path

INPUT_FILE_PATH = Path(__file__).parent


class ServerRackGraph:
    def __init__(self) -> None: ...


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> ServerRackGraph:
    # Create graph class
    graph = ServerRackGraph()

    for line in file_content:
        device, raw_output_devices = line.split(":")
        output_devices = raw_output_devices.split()

        # Add device to graph and also connections

    return graph


def solve_01(data: ServerRackGraph) -> int:
    # DFS (Recursive) Approach (Most Common)
    #    Start: Begin at the source node.
    #    Mark & Add: Mark the current node as visited and add it to the current path.
    #    Explore Neighbors: For each unvisited neighbor of the current node:
    #    If neighbor is the target: You've found a complete path. Record it.
    #    If neighbor is not the target: Recursively call the function for that neighbor.
    #    Backtrack: After exploring all neighbors, unmark the current node and remove it from the path to explore other possibilities.
    # Key Considerations
    #    Cycles: Crucial to track visited nodes within a single path to avoid infinite loops in cyclic graphs (e.g., A -> B -> A -> ...).
    #    Data Structures: Use a list or stack to build the current path and a list of lists/stacks to store all found paths.
    #    Efficiency: Finding all paths can be computationally expensive (exponential time) for dense graphs, as the number of paths can grow very quickly.
    return


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the example 1 is {solution}")  # Solution 5
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the part 1 is {solution}")  # Solution


if __name__ == "__main__":
    main()
