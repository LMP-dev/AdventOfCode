from pathlib import Path

DATA_FILE_NAME = "input.txt"
INPUT_FILE = Path(__file__).parent / DATA_FILE_NAME
TEST_INPUT_FILE = Path(__file__).parent / "example_1.txt"


def parse_input(file_path: Path) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def is_it_a_number(character: str) -> tuple[bool, int | str]:
    try:
        number = int(character)
    except ValueError:
        return (False, character)
    else:
        return (True, number)


def solve_01(data: list[str]) -> int:
    calibration_values = []
    for line in data:
        first = None
        last = None
        for begining, end in zip(line, reversed(line)):
            if not first:
                is_number, val = is_it_a_number(begining)
                if is_number:
                    first = val
            if not last:
                is_number, val = is_it_a_number(end)
                if is_number:
                    last = val
        calibration_values.append(10 * first + last)
    return sum(calibration_values)


def main() -> None:
    data = parse_input(INPUT_FILE)
    solution = solve_01(data)
    print(solution)


if __name__ == "__main__":
    main()
