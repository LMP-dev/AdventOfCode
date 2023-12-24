from pathlib import Path
import time
from functools import partial

from scipy.optimize import fsolve, newton

INPUT_FILE = Path(__file__).parent / "input.txt"
# INPUT_FILE = Path(__file__).parent / "test_input.txt"  # sol = 301


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


def equation_monkey(
    number_monkeys: dict, math_monkeys: dict, monkey: str, result: int, humn_guess: int
) -> int:
    number_monkeys["humn"] = humn_guess
    return monkey_yells(number_monkeys, math_monkeys, monkey) - result


def main():
    number_monkeys, math_monkeys = parse_input(INPUT_FILE)
    number_monkeys["humn"] = None  # in order to find which part of root have "humn"
    operation = math_monkeys["root"]
    monkey_1 = operation[0:4]
    monkey_2 = operation[7:]
    try:
        result = monkey_yells(number_monkeys, math_monkeys, monkey_1)
        monkey_to_check = monkey_2

    except TypeError:
        result = monkey_yells(number_monkeys, math_monkeys, monkey_2)
        monkey_to_check = monkey_1

    part_2 = newton(
        partial(equation_monkey, number_monkeys, math_monkeys, monkey_to_check, result),
        20000,
        disp=True,
    )
    print(f"result is: {result}")
    print(f"Human guess should be: {part_2}")
    number_monkeys["humn"] = part_2
    print(
        f"monkey 1 - {monkey_1} yells: {monkey_yells(number_monkeys, math_monkeys, monkey_1)}"
    )
    print(
        f"monkey 2 - {monkey_2} yells: {monkey_yells(number_monkeys, math_monkeys, monkey_2)}"
    )


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"--- {(time.time() - start) * 1000} ms ---")
