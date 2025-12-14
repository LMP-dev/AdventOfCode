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
    ranges: list[tuple[int, int]] = []
    ingredient_ids: list[int] = []

    split_mode = True

    for line in file_content:
        if line == "":
            split_mode = False
            continue
        if split_mode:
            start, end = line.split("-")
            ranges.append((int(start), int(end)))
        else:
            ingredient_ids.append(int(line))
    return ranges, ingredient_ids


def merge_overlaped_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Returns an ordered range list without overlaped ranges completely inside others"""
    ordered_ranges = sorted(ranges)
    simplified_ranges: list[tuple[int, int]] = []
    last_start, last_end = None, None

    for start, end in ordered_ranges:
        if last_start is None:
            last_start = start
            last_end = end
            simplified_ranges.append((start, end))
            continue
        if start < last_end and end <= last_end:
            continue
        else:
            last_start = start
            last_end = end
            simplified_ranges.append((start, end))

    return simplified_ranges


def solve_01(data: Any) -> int:
    ranges, ingredients_ids = data
    # Remove overlaped range values
    simplified_ranges = merge_overlaped_ranges(ranges)

    count = 0
    start_range = [a for a, _ in simplified_ranges]
    end_range = [b for _, b in simplified_ranges]
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
    print(f"The solution of the part 1 is {solution}")  # solution 798


if __name__ == "__main__":
    main()
