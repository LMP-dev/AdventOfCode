# Standard library
from pathlib import Path

INPUT_FILE_PATH = Path(__file__).parent


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []

    for line in file_content:
        if line == "":
            break
        start, end = line.split("-")
        ranges.append((int(start), int(end)))
    return ranges


def merge_overlaped_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Returns an ordered range list without overlaped ranges completely inside others"""
    ordered_ranges = sorted(ranges)
    no_overlaped_ranges: list[tuple[int, int]] = []
    last_start, last_end = None, None

    for start, end in ordered_ranges:
        if last_start is None:
            last_start = start
            last_end = end
            no_overlaped_ranges.append((start, end))
            continue
        if start < last_end and end <= last_end:
            continue
        else:
            last_start = start
            last_end = end
            no_overlaped_ranges.append((start, end))

    return no_overlaped_ranges


def simplify_ranges(ordered_ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Considers no overlaped ranges are present and ranges are ordered"""
    simplified_ranges: list[tuple[int, int]] = []

    last_start, last_end = None, None

    for start, end in ordered_ranges:
        if last_start is None:
            last_start = start
            last_end = end
            simplified_ranges.append((start, end))
        if start <= last_end and end >= last_end:
            simplified_ranges.pop(-1)  # extract last tuple to add the extended one
            simplified_ranges.append((last_start, end))
            last_end = end
            continue
        else:
            last_start = start
            last_end = end
            simplified_ranges.append((start, end))

    return simplified_ranges


def solve_02(data: list[tuple[int, int]]) -> int:
    ranges = data
    # Remove overlaped range values
    no_overlaped_ranges = merge_overlaped_ranges(ranges)
    # Merge ranges
    simplified_ranges = simplify_ranges(no_overlaped_ranges)

    count = 0
    for start, end in simplified_ranges:
        count += end - start + 1  # Number of IDs in range

    return count


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the example 1 is {solution}")  # Solution 14
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the part 2 is {solution}")  # Solution 366181852921027

    # file_content = read_data(INPUT_FILE_PATH / "test.txt")
    # data = parse_input(file_content)
    # solution = solve_02(data)
    # print(f"The solution of the example 1 is {solution}")  # Solution 14


if __name__ == "__main__":
    main()
