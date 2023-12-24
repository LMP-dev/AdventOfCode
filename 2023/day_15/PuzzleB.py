# Standard library
from pathlib import Path
from dataclasses import dataclass, field

INPUT_FILE_PATH = Path(__file__).parent


@dataclass
class Lens:
    label: str
    focal_length: int

    def __eq__(self, other):
        if isinstance(other, Lens):
            return self.label == other.label
        elif isinstance(other, str):
            return self.label == other
        else:
            raise Exception(
                f"Comparison for Lens class only available for Lens or str instances. Tryied with {type(other)}"
            )


@dataclass
class Box:
    lenses: list[Lens] = field(default_factory=list)

    def remove_lens(self, lens_label: str) -> None:
        if lens_label in self.lenses:
            self.lenses.remove(lens_label)

    def add_lens(self, new_lens: Lens) -> None:
        if new_lens in self.lenses:
            i = self.lenses.index(new_lens)
            self.lenses.remove(new_lens)
            self.lenses.insert(i, new_lens)
        else:
            self.lenses.append(new_lens)


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> list[tuple[str, str, int | None]]:
    raw_initialization_sequence = file_content[0]
    initialization_sequence = raw_initialization_sequence.split(",")
    parsed_ini_sequence = []
    for sequence in initialization_sequence:
        seq_split = sequence.split("=")
        if len(seq_split) == 1:
            label = seq_split[0].replace("-", "")
            operation = "-"
            value = None
            parsed_ini_sequence.append((label, operation, value))
        else:
            label = seq_split[0]
            operation = "="
            value = int(seq_split[1])
            parsed_ini_sequence.append((label, operation, value))
    return parsed_ini_sequence


def hash_algorithm(sequence: str) -> int:
    current_value = 0

    for char in sequence:
        # Determine ASCII code
        asci = ord(char)
        # Increase current value by ASCII code
        current_value += asci
        # Multiply current value by 17
        current_value *= 17
        # Set to reminder divinding by 256
        current_value %= 256
    return current_value


def calculate_focusing_power(box_pos: int, slot: int, focal_lenght: int) -> int:
    """Slots must start at index 1!!!"""
    return (box_pos + 1) * slot * focal_lenght


def calculate_box_focusing_power(box_pos: int, lenses: list[Lens]) -> int:
    box_focusing_power = 0
    for i, lens in enumerate(lenses):
        box_focusing_power += calculate_focusing_power(
            box_pos, i + 1, lens.focal_length
        )

    return box_focusing_power


def solve_02(data: list[tuple[str, str, int | None]]) -> int:
    # Initialization boxes and lens
    boxes = {i: Box() for i in range(256)}

    for sequence in data:
        label, operation, focal_length = sequence
        box_number = hash_algorithm(label)
        box = boxes[box_number]
        if operation == "-":
            box.remove_lens(label)
        elif operation == "=":
            lens = Lens(label, focal_length)
            box.add_lens(lens)

    filled_boxes = {i: box for i, box in boxes.items() if box.lenses}

    focusing_power = 0
    for box_pos, box in filled_boxes.items():
        focusing_power += calculate_box_focusing_power(box_pos, box.lenses)

    return focusing_power


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the example 1 is {solution}")
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the part 2 is {solution}")


if __name__ == "__main__":
    main()
