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


def _clean_first_list(
    first_list: list[int], second_list: list[int], inverse_lists: bool
) -> tuple[list[int], list[int]]:
    last_value = None
    last_repeated_value = None
    repeated_indexes: list[list[int]] = []
    temp_index: list[int] = []

    # Identify repeated values
    for index, value in enumerate(first_list):
        if value == last_value:
            if value == last_repeated_value:
                temp_index.append(index)
            else:
                temp_index.append(index - 1)
                temp_index.append(index)
                last_repeated_value = value
        else:
            if temp_index:
                repeated_indexes.append(temp_index)
            temp_index = []  # reset temporal list
        last_value = value

    # Remove repeated values
    first_cleaned = first_list.copy()
    second_cleaned = second_list.copy()
    repeated_indexes.reverse()  # To start from end list so first indexes are mantained

    for indexes in repeated_indexes:
        to_remove = []
        max_value = None
        last_index = None
        for index in indexes:
            if max_value is None:
                max_value = second_list[index]
                last_index = index
            else:
                if inverse_lists:
                    if max_value > second_list[index]:
                        to_remove.append(last_index)
                        max_value = second_list[index]
                        last_index = index
                    else:
                        to_remove.append(index)
                else:
                    if max_value < second_list[index]:
                        to_remove.append(last_index)
                        max_value = second_list[index]
                        last_index = index
                    else:
                        to_remove.append(index)
        # Remove from cleaned lists
        ordered_to_remove = reversed(sorted(to_remove))

        for k in ordered_to_remove:
            _ = first_cleaned.pop(k)
            _ = second_cleaned.pop(k)

    return first_cleaned, second_cleaned


def remove_repeated_values(
    first_range: list[int], second_range: list[int]
) -> tuple[list[int], list[int]]:
    if len(first_range) != len(set(first_range)) or len(second_range) != len(
        set(second_range)
    ):
        print("THERE IS REPEATED STARTING RANGE NUMBERS!")
        # Treat start ranges
        temp_start, temp_end = _clean_first_list(first_range, second_range, False)
        # Treat end ranges
        end_range, start_range = _clean_first_list(temp_end, temp_start, True)

        return start_range, end_range
    return first_range, second_range


def solve_01(data: Any) -> int:
    ordered_ranges, ingredients_ids = data
    # Remove overlaped range values
    start_range, end_range = remove_repeated_values(
        [a for a, _ in ordered_ranges], [b for _, b in ordered_ranges]
    )

    count = 0
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
    print(f"The solution of the part 1 is {solution}")  # solution (is higher than 775)


if __name__ == "__main__":
    main()
