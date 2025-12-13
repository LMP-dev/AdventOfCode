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
    pairs: list[tuple[tuple[int, int, int], tuple[int, int, int]]], max_connections: int
) -> list[list[tuple[int, int, int]]]:
    circuits: list[list[tuple[int, int, int]]] = []

    for i, (p1, p2) in enumerate(pairs):
        # print(f"For connection {i +1} the pair of points is: ({p1}, {p2})")

        if i >= max_connections:
            break
        p1_location = [p1 in circuit for circuit in circuits]
        p2_location = [p2 in circuit for circuit in circuits]
        # Case both points are in circuits
        if any(p1_location) and any(p2_location):
            # print("Found both points inside a circuit!")
            index_point_p1 = p1_location.index(True)
            index_point_p2 = p2_location.index(True)
            # Both in same circuit
            if index_point_p1 == index_point_p2:
                # print(">>> Both points inside the same circuit")
                # print(f"After making connection {i+1}, the circuits are {circuits}")
                continue
            # On different circuits
            # print(">>> Points in different circuits")
            if index_point_p1 > index_point_p2:
                p1_circuit = circuits.pop(index_point_p1)
                circuits[index_point_p2].extend(p1_circuit)  # Fuse circuits
            else:
                p2_circuit = circuits.pop(index_point_p2)
                circuits[index_point_p1].extend(p2_circuit)  # Fuse circuits

        # Case only one point in circuits
        elif any(p1_location):
            # print("Found first point inside a circuit!")
            index_point_p1 = p1_location.index(True)
            circuits[index_point_p1].append(p2)  # Add missing point to circuit

        # Case only one point in circuits
        elif any(p2_location):
            # print("Found second point inside a circuit!")
            index_point_p2 = p2_location.index(True)
            circuits[index_point_p2].append(p1)  # Add missing point to circuit

        # Case no points in circuits
        else:
            # print("No points found in a circuit!")
            circuits.append([p1, p2])  # Add both points as new circuit

        # print(f"After making connection {i+1}, the circuits are {circuits}")

    return circuits


def solve_01(data: list[tuple[int, int, int]], max_connections: int) -> int:
    # Calculate all distances between points
    pairs_of_points = list(combinations(data, 2))
    # print(f"The pairs of points are: {pairs_of_points}")
    distances = {pair: calculate_distance(pair) for pair in pairs_of_points}

    # Sort by distances
    sorted_distances = {
        k: v for k, v in sorted(distances.items(), key=lambda item: item[1])
    }  # item[1] represents the sorting based on value

    # Create circuits
    circuits = create_circuits(sorted_distances.keys(), max_connections)

    # calculate 3 highest circuits sizes
    sorted_circuits = sorted(circuits, key=len, reverse=True)

    # print(f"the sorted circuits created are: {sorted_circuits}")

    return len(sorted_circuits[0]) * len(sorted_circuits[1]) * len(sorted_circuits[2])


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_01(data, 10)
    print(f"The solution of the example 1 is {solution}")  # Solution 40
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_01(data, 1000)
    print(f"The solution of the part 1 is {solution}")

    # file_content = read_data(INPUT_FILE_PATH / "tests.txt")
    # data = parse_input(file_content)
    # solution = solve_01(data)
    # print(f"The solution of the example 1 is {solution}")


if __name__ == "__main__":
    main()
