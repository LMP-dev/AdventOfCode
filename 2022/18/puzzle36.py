from pathlib import Path
import time
from collections import deque


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


def is_not_hole(
    rock: tuple[int],
    rocks: list[tuple[int]],
    x_range: tuple[int],
    y_range: tuple[int],
    z_range: tuple[int],
) -> bool:
    x_max, x_min = x_range
    y_max, y_min = y_range
    z_max, z_min = z_range
    queue = deque()
    queue.append(rock)
    visited = set()
    while queue:
        rock = queue.popleft()
        if rock in visited:
            continue
        visited.add(rock)
        if rock in rocks:
            continue
        x, y, z = rock
        if (
            x >= x_max
            or x <= x_min
            or y >= y_max
            or y <= y_min
            or z >= z_max
            or z <= z_min
        ):
            return True
        for neigh in generate_around_cubes(rock):
            queue.append(neigh)
    return False


def main():
    cubes = parse_input(INPUT_FILE)
    x_cords = [x for x, y, z in cubes]
    y_cords = [y for x, y, z in cubes]
    z_cords = [z for x, y, z in cubes]
    x_max, x_min = max(x_cords), min(x_cords)
    y_max, y_min = max(y_cords), min(y_cords)
    z_max, z_min = max(z_cords), min(z_cords)

    connections = 0
    for cube in cubes:
        neighbours = generate_around_cubes(cube)
        for neigh in neighbours:
            if neigh not in cubes:
                if is_not_hole(
                    neigh, cubes, (x_max, x_min), (y_max, y_min), (z_max, z_min)
                ):
                    connections += 1

    print(f"Total connections: {connections}")


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"--- {(time.time() - start) * 1000} ms ---")
