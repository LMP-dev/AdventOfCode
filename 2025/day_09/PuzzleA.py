# Standard library
from pathlib import Path
from itertools import combinations

INPUT_FILE_PATH = Path(__file__).parent


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> list[tuple[int, int]]:
    return [tuple(map(int, line.split(","))) for line in file_content]


def calculate_area(
    pair: tuple[tuple[int, int], tuple[int, int]],
) -> int:
    p1, p2 = pair
    side_a = abs(p1[0] - p2[0]) + 1
    side_b = abs(p1[1] - p2[1]) + 1
    return side_a * side_b


def solve_01(data: list[tuple[int, int]]) -> int:
    # Calculate all areas between rectangles
    pairs_of_points = list(combinations(data, 2))
    areas = {pair: calculate_area(pair) for pair in pairs_of_points}

    # Sort by areas from high to low
    sorted_areas = {
        k: v for k, v in sorted(areas.items(), key=lambda item: item[1], reverse=True)
    }

    biggest_rectangle = list(sorted_areas.keys())[0]
    biggest_area = list(sorted_areas.values())[0]

    print(f"the bissgest rectangle is formed by points: {biggest_rectangle}")

    return biggest_area


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the example 1 is {solution}")  # Solution 50
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the part 1 is {solution}")  # Solution 4776487744


if __name__ == "__main__":
    main()
