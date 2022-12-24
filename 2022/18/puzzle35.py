from pathlib import Path
import time

start = time.time()

INPUT_FILE = Path(__file__).parent / "input.txt"
# INPUT_FILE = Path(__file__).parent / "test_input.txt"  # Solution = 64


def parse_input(file_path: Path) -> list[tuple[int]]:
    coordinates = list()
    with open(file_path, "r") as file:
        for line in file:
            cords = line.strip().split(",")
            coordinates.append(tuple(map(int, cords)))
    return coordinates


def generate_around_cubes(cube: tuple[int]) -> list[tuple[int]]:
    cubes = [
        (cube[0] + 1, cube[1], cube[2]),
        (cube[0] - 1, cube[1], cube[2]),
        (cube[0], cube[1] + 1, cube[2]),
        (cube[0], cube[1] - 1, cube[2]),
        (cube[0], cube[1], cube[2] + 1),
        (cube[0], cube[1], cube[2] - 1),
    ]
    return cubes


def main():
    cubes = parse_input(INPUT_FILE)
    connections = 0
    for cube in cubes:
        neighbours = generate_around_cubes(cube)
        for neigh in neighbours:
            if neigh not in cubes:
                connections += 1

    print(f"Total connections: {connections}")


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"--- {(time.time() - start) * 1000} ms ---")
