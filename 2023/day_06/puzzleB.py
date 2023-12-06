from pathlib import Path
import re

INPUT_FILE_PATH = Path(__file__).parent


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> tuple[int, int]:
    _, times = file_content[0].split(":")
    _, distances = file_content[1].split(":")
    match_times = re.findall(r"\d+", times)
    match_distances = re.findall(r"\d+", distances)
    time = ""
    distance = ""
    for time_str, distance_str in zip(match_times, match_distances):
        time += time_str
        distance += distance_str
    return (int(time), int(distance))


def solve_01(data: list[tuple[int, int]]) -> int:
    ways_to_win = 0
    time, max_dist = data
    for hold_time in range(time):
        time_to_race = time - hold_time
        distance = hold_time * time_to_race
        if distance > max_dist:
            ways_to_win += 1
    return ways_to_win


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the example is {solution}")
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of part 1 is {solution}")


if __name__ == "__main__":
    main()
