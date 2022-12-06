from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input.txt"


def is_all_different(buffer: list[str]) -> bool:
    unrepeated_elements = set(buffer)
    return len(unrepeated_elements) == 4


def identify_beginning_buffer(stream: str) -> int:
    marker = list()
    for i, char in enumerate(stream):
        # Fill until 3 buffer characters
        if len(marker) < 3:
            marker.append(char)
        else:
            marker.append(char)
            if is_all_different(marker):
                return i + 1
            marker.pop(0)


def main() -> None:
    with open(INPUT_FILE, "r") as file:
        stream = next(file)
        buffer_pos = identify_beginning_buffer(stream)

    print(buffer_pos)


if __name__ == "__main__":
    main()
