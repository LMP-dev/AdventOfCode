from pathlib import Path
from dataclasses import dataclass
import math

INPUT_FILE_PATH = Path(__file__).parent


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> list[tuple[int, int]]:
    _, times = file_content[0].split(":")
    _, distances = file_content[1].split(":")
    raw_times_list = times.strip().split(" ")
    raw_distances_list = distances.strip().split(" ")
    times_list = []
    distances_list = 
    return [(int(time), int(dist)) for time, dist in zip(times_list, distances_list)]


def solve_01(data: list[tuple[int, int]]) -> int:
    number_ways_to_win = []
    product = 1
    for race in data:
        ways_to_win = 0
        time, max_dist = race
        for hold_time in range(time):
            time_to_race = time - hold_time
            distance = hold_time * time_to_race
            if distance > max_dist:
                ways_to_win += 1
        number_ways_to_win.append(ways_to_win)
        product *= ways_to_win
    return product


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the example is {solution}")
    data = parse_input(INPUT_FILE_PATH / "input.txt")
    solution = solve_01(data)
    print(f"The solution of part 1 is {solution}")


if __name__ == "__main__":
    main()
