# Standard library
from pathlib import Path
from itertools import combinations
import math

INPUT_FILE_PATH = Path(__file__).parent


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> list[tuple[int, int, int]]:
    points_in_space: list[tuple[int, int, int]] = []

    for line in file_content:
        points_in_space.append(tuple(map(int, line.split(","))))

    return points_in_space


def calculate_distance(
    pair: tuple[tuple[int, int, int], tuple[int, int, int]],
) -> int:
    p1, p2 = pair
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)


def create_circuits(
    pairs: list[tuple[tuple[int, int, int], tuple[int, int, int]]],
) -> list[list[tuple[int, int, int]]]:
    circuits: list[list[tuple[int, int, int]]] = []

    for pair in pairs:
        # Case no point in circuits

        # Case only one point in circuits

        # Case both points are in circuits
        #     both in same circuit
        #     on different circuits

        ...

    # any(x in list for list in circuits)  # circuits of 1 apart or not needed?


def solve_01(data: list[tuple[int, int, int]]) -> int:
    # Calculate all distances between points
    pairs_of_points = list(combinations(data, 2))
    print(f"The pairs of points are: {pairs_of_points}")
    distances = {pair: calculate_distance(pair) for pair in pairs_of_points}

    # Sort by distances
    sorted_distances = {
        k: v for k, v in sorted(distances.items(), key=lambda item: item[1])
    }  # item[1] represents the sorting based on value

    # Create circuits
    circuits = create_circuits(sorted_distances.keys())

    # calculate 3 highest circuits sizes
    sorted_circuits = sorted(circuits, key=len, reverse=True)

    return len(sorted_circuits[0]) + len(sorted_circuits[1]) + len(sorted_circuits[2])


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the example 1 is {solution}")  # Solution 40
    # file_content = read_data(INPUT_FILE_PATH / "input.txt")
    # data = parse_input(file_content)
    # solution = solve_01(data)
    # print(f"The solution of the part 1 is {solution}")

    # file_content = read_data(INPUT_FILE_PATH / "tests.txt")
    # data = parse_input(file_content)
    # solution = solve_01(data)
    # print(f"The solution of the example 1 is {solution}")


if __name__ == "__main__":
    main()
