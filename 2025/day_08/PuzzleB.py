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


def create_one_circuits(
    pairs: list[tuple[tuple[int, int, int], tuple[int, int, int]]],
    list_of_points: list[tuple[int, int, int]],
) -> list[list[tuple[int, int, int]]]:
    circuits: list[list[tuple[int, int, int]]] = []
    single_circuits = list_of_points.copy()
    last_pair = None

    for i, (p1, p2) in enumerate(pairs):
        if len(single_circuits) + len(circuits) == 1:
            break

        p1_location = [p1 in circuit for circuit in circuits]
        p2_location = [p2 in circuit for circuit in circuits]
        # Case both points are in circuits
        if any(p1_location) and any(p2_location):
            index_point_p1 = p1_location.index(True)
            index_point_p2 = p2_location.index(True)
            # Both in same circuit
            if index_point_p1 == index_point_p2:
                continue
            # On different circuits
            if index_point_p1 > index_point_p2:
                p1_circuit = circuits.pop(index_point_p1)
                circuits[index_point_p2].extend(p1_circuit)  # Fuse circuits
            else:
                p2_circuit = circuits.pop(index_point_p2)
                circuits[index_point_p1].extend(p2_circuit)  # Fuse circuits
            last_pair = (p1, p2)

        # Case only one point in circuits
        elif any(p1_location):
            index_point_p1 = p1_location.index(True)
            circuits[index_point_p1].append(p2)  # Add missing point to circuit

            single_circuits.remove(p2)
            last_pair = (p1, p2)

        # Case only one point in circuits
        elif any(p2_location):
            index_point_p2 = p2_location.index(True)
            circuits[index_point_p2].append(p1)  # Add missing point to circuit

            single_circuits.remove(p1)
            last_pair = (p1, p2)

        # Case no points in circuits
        else:
            circuits.append([p1, p2])  # Add both points as new circuit

            single_circuits.remove(p1)
            single_circuits.remove(p2)
            last_pair = (p1, p2)

    return last_pair


def solve_02(data: list[tuple[int, int, int]]) -> int:
    # Calculate all distances between points
    pairs_of_points = list(combinations(data, 2))
    distances = {pair: calculate_distance(pair) for pair in pairs_of_points}

    # Sort by distances
    sorted_distances = {
        k: v for k, v in sorted(distances.items(), key=lambda item: item[1])
    }  # item[1] represents the sorting based on value

    # Create circuits
    last_pair = create_one_circuits(sorted_distances.keys(), data)
    print(f"The last pair to be connected was: {last_pair}")

    # Calculatedistance by multiplying the X coordinates
    return last_pair[0][0] * last_pair[1][0]


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the example 1 is {solution}")  # Solution 25272
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the part 2 is {solution}")  # Solution 1474050600


if __name__ == "__main__":
    main()
