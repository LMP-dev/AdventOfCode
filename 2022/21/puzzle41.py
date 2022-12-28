from pathlib import Path
import time

start = time.time()

INPUT_FILE = Path(__file__).parent / "input.txt"
# INPUT_FILE = Path(__file__).parent / "test_input.txt"  # sol = 152


def parse_input(file_path: Path) -> list[int]:
    math_monkeys = dict()
    number_monkeys = dict()
    with open(file_path, "r") as file:
        for line in file:
            monkey, result = line.split(":")
            try:
                number = int(result)
                number_monkeys.update({monkey: number})
            except ValueError:
                operation = result.strip()
                math_monkeys.update({monkey: operation})
    return number_monkeys, math_monkeys


def monkey_yells(number_monkeys: dict, math_monkeys: dict, monkey: str) -> int:
    try:
        return number_monkeys[monkey]
    except KeyError:
        operation = math_monkeys[monkey]
        monkey_1 = operation[0:4]
        monkey_1_number = monkey_yells(number_monkeys, math_monkeys, monkey_1)
        operator = operation[5]
        monkey_2 = operation[7:]
        monkey_2_number = monkey_yells(number_monkeys, math_monkeys, monkey_2)
        if operator == "+":
            return monkey_1_number + monkey_2_number
        elif operator == "*":
            return monkey_1_number * monkey_2_number
        elif operator == "-":
            return monkey_1_number - monkey_2_number
        elif operator == "/":
            return monkey_1_number / monkey_2_number


def main():
    number_monkeys, math_monkeys = parse_input(INPUT_FILE)
    part_1 = monkey_yells(number_monkeys, math_monkeys, "root")
    print(part_1)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"--- {(time.time() - start) * 1000} ms ---")
