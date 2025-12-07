# Standard library
from pathlib import Path
from typing import Any

INPUT_FILE_PATH = Path(__file__).parent


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> Any:
    ordered_ranges: list[tuple[int, int]] = []
    ingredient_ids: list[int] = []

    split_mode = True

    for line in file_content:
        if line == "":
            split_mode = False
            continue
        if split_mode:
            start, end = line.split("-")
            ordered_ranges.append((int(start), int(end)))
        else:
            ingredient_ids.append(int(line))
    return sorted(ordered_ranges), ingredient_ids


def solve_01(data: Any) -> int:
    ordered_ranges, ingredients_ids = data
    count = 0

    # Fusion repeated starting and ending ranges

    start_range = [a for a, _ in ordered_ranges]
    end_range = [b for _, b in ordered_ranges]

    # if len(start_range) != len(set(start_range)):
    #     raise Exception("THERE IS REPEATED STARTING RANGE NUMBERS!")
    # if len(end_range) != len(set(end_range)):
    #     raise Exception("THERE IS REPEATED ENDING RANGE NUMBERS!")

    for id in ingredients_ids:
        for i, start in enumerate(start_range):
            if id <= start:
                if id == start:
                    beginning = start
                    end = end_range[i]
                else:
                    beginning = start_range[i - 1]
                    end = end_range[i - 1]
                if id >= beginning and id <= end:
                    count += 1

        # Check for last range
        if id > start:  # avoids last id equal to beginning range
            if id >= start_range[-1] and id <= end_range[-1]:
                count += 1

    return count


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_01(data)  # Solution 3
    print(f"The solution of the example 1 is {solution}")
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the part 1 is {solution}")  # solution 775


if __name__ == "__main__":
    main()
