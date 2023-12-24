from __future__ import annotations
from pathlib import Path
import re
from math import lcm


INPUT_FILE = Path(__file__).parent / "input.txt"
# INPUT_FILE = Path(__file__).parent / "test_input.txt"


class Monkey:
    def __init__(
        self,
        items: list[int],
        operation: str,
        divider: int,
        true: int,
        false: int,
    ) -> None:
        self.items = items
        self.operation = operation
        self.test = divider
        self.true = true
        self.false = false
        self.count = 0

    def do_turn(self, monkeys: list[Monkey], lcm_worry: int) -> None:
        while self.items:
            # Takes item
            old = self.items.pop(0)
            # Inspects item
            item = eval(self.operation)
            self.count += 1
            # Relive
            item = item % lcm_worry
            # Test
            monkey_num = self.true if item % self.test == 0 else self.false
            # Throw
            monkeys[monkey_num].catch_item(item)

    def catch_item(self, item: int) -> None:
        self.items.append(item)


def count_monkey_bussiness(monkeys: list[Monkey]) -> int:
    counts = [monkey.count for monkey in monkeys]
    counts.sort(reverse=True)
    return counts[0] * counts[1]


def create_monkeys(monkeys: list[dict]) -> list[Monkey]:
    return [Monkey(**monkey) for monkey in monkeys]


def parse_input(file: Path) -> list[dict]:
    monkeys = list()
    with open(INPUT_FILE, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("Monkey "):
                monkey = dict()
            elif line.startswith("Starting items:"):
                items_str = line.split(": ")[1]
                monkey["items"] = [int(val) for val in items_str.split(",")]
            elif line.startswith("Operation:"):
                operation = line.split("new = ")
                monkey["operation"] = operation[1]
            elif line.startswith("Test:"):
                numbers = re.findall("[0-9]+", line)
                divider = numbers[0]
                monkey["divider"] = int(divider)
            elif line.startswith("If true:"):
                numbers = re.findall("[0-9]+", line)
                true_monkey = numbers[0]
                monkey["true"] = int(true_monkey)
            elif line.startswith("If false:"):
                numbers = re.findall("[0-9]+", line)
                false_monkey = numbers[0]
                monkey["false"] = int(false_monkey)
                monkeys.append(monkey)
    return monkeys


def main() -> None:
    monkeys_raw = parse_input(INPUT_FILE)
    monkeys = create_monkeys(monkeys_raw)
    worry_base = lcm(*(monkey.test for monkey in monkeys))
    for _ in range(10000):
        for monkey in monkeys:
            monkey.do_turn(monkeys, worry_base)
    print(count_monkey_bussiness(monkeys))


if __name__ == "__main__":
    main()
