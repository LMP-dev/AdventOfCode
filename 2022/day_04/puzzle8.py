from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input.txt"


def parse_line(line: str) -> tuple[set[int]]:
    def transform_to_set(assignment: str) -> set[int]:
        start, stop = assignment.split("-")
        return set(range(int(start), int(stop) + 1))

    assignment_1, assignment_2 = line.split(",")
    return transform_to_set(assignment_1), transform_to_set(assignment_2)


def main() -> None:
    overlaped_pairs = 0
    with open(INPUT_FILE, "r") as file:
        for line in file:
            # Parse line
            elf_bob, elf_chad = parse_line(line)
            # Compare sets
            if elf_bob.intersection(elf_chad):
                overlaped_pairs += 1

    print(overlaped_pairs)


if __name__ == "__main__":
    main()
