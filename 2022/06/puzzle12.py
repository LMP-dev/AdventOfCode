from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input.txt"


def is_all_different(message: list[str]) -> bool:
    unrepeated_elements = set(message)
    return len(unrepeated_elements) == 14


def identify_beginning_message(stream: str) -> int:
    marker = list()
    for i, char in enumerate(stream):
        # Fill until 13 message characters
        if len(marker) < 13:
            marker.append(char)
        else:
            marker.append(char)
            if is_all_different(marker):
                return i + 1
            marker.pop(0)


def main() -> None:
    with open(INPUT_FILE, "r") as file:
        stream = next(file)
        message_pos = identify_beginning_message(stream)

    print(message_pos)


if __name__ == "__main__":
    main()
