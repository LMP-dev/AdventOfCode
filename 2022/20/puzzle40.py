from pathlib import Path
import time
from collections import deque

start = time.time()

INPUT_FILE = Path(__file__).parent / "input.txt"
# INPUT_FILE = Path(__file__).parent / "test_input.txt"  # sol = 1623178306

DECRYPTION_KEY = 811589153


def parse_input(file_path: Path) -> list[int]:
    with open(file_path, "r") as file:
        list_numbers = list(map(int, file.readlines()))
    return list_numbers


def mix(list_numbers: deque[tuple[int]]) -> deque[tuple[list]]:
    lenght_list = len(list_numbers)
    for i in range(lenght_list):
        # rotate queue to start with number
        while list_numbers[0][0] != i:
            list_numbers.append(list_numbers.popleft())
        # pop number and calculate new position
        current_number = list_numbers.popleft()
        rotate_by = current_number[1] % (lenght_list - 1)
        # rotate queue to start with current number
        for _ in range(rotate_by):
            list_numbers.append(list_numbers.popleft())
        list_numbers.append(current_number)
    return list_numbers


def main():
    numbers = parse_input(INPUT_FILE)
    list_numbers = deque((i, num * DECRYPTION_KEY) for i, num in enumerate(numbers))
    for _ in range(10):
        list_numbers = mix(list_numbers)

    # Calculate score
    while list_numbers[0][1] != 0:
        list_numbers.append(list_numbers.popleft())
    part_2 = sum(list_numbers[num % len(list_numbers)][1] for num in [1000, 2000, 3000])
    print(part_2)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"--- {(time.time() - start) * 1000} ms ---")
