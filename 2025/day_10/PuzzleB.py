# Standard library
from pathlib import Path
import math
import copy
from itertools import combinations


INPUT_FILE_PATH = Path(__file__).parent


class MachineJoltage:
    def __init__(
        self,
        buttons_schematic: list[tuple[int, ...]],
        joltage_requirements: tuple[int, ...],
    ):
        """
        self.joltage_buttons data structure is a list where each element contains
        all the buttons that activate the counter in the same index position.
        The buttons are stored as a dict with k=tuple(index the button activates)
        and v=max repetitions allowed for that button.

        max repetitions allowed for a button are calculated as the minimum joltage
        of all the counters this button modifies
        """
        self.target_counter = joltage_requirements

        self.joltage_buttons: list[dict[tuple[int, ...], int]] = [
            dict() for _ in range(len(joltage_requirements))
        ]
        self.min_btn_pressed = math.inf

        # Prepare buttons affecting each joltage value
        for scheme in buttons_schematic:
            min_joltage = min([self.target_counter[i] for i in scheme])
            for index in scheme:
                self.joltage_buttons[index].update({scheme: min_joltage})

    @staticmethod
    def _sum_tuples(t1: tuple[int, ...], t2: tuple[int, ...]) -> tuple[int, ...]:
        return tuple([a + b for a, b in zip(t1, t2)])

    @staticmethod
    def _increase_counter(
        counter: tuple[int, ...], btns_combination: tuple[tuple[int, ...]]
    ) -> tuple[int, ...]:
        temp_counter = list(counter)
        for button in btns_combination:
            for index in button:
                temp_counter[index] += 1
        return tuple(temp_counter)

    def _allowed_combinations(
        self,
        index: int,
        counter: tuple[int, ...],
        buttons: list[list[dict[tuple[int, ...], int]]],
    ) -> list[tuple[tuple[int, ...]]]:
        diff_counter = tuple(
            [self.target_counter[i] - counter[i] for i in range(len(counter))]
        )
        # TODO
        min_counter = min(diff_counter)
        min_counter_index = list(diff_counter).index(min_counter)

        ...

    def _recursion_btns_calculation(
        self,
        counter: tuple[int, ...],
        btns_pressed: int,
        buttons_distribution: list[list[dict[tuple[int, ...], int]]],
    ):
        # Select next counter to fill
        # TODO
        # Identify columns only 1 button
        # If not select min diff column not empty
        index = list(self.target_counter).index(min(self.target_counter))

        # Create allowed combinations considering the max repetition of elements
        allowed_btns_combinations = self._allowed_combinations(
            index, counter, buttons_distribution
        )

        # Loop through all options
        for btns_combination in allowed_btns_combinations:
            # Increase btns_pressed count
            new_btns_pressed = btns_pressed + len(btns_combination)

            # Increase counter
            new_counter = self._sum_tuples(counter, btns_combination)

            # Guard clauses to stop recursion
            if any(now > target for now, target in zip(counter, self.target_counter)):
                return
            if counter == self.target_counter:
                if new_btns_pressed < self.min_btn_pressed:
                    self.min_btn_pressed = new_btns_pressed
                return

            # Remove buttons used from buttons_distribution
            # TODO
            copy_buttons = copy.deepcopy(buttons_distribution)
            new_buttons_distribution = ...

            # Call again function
            self._recursion_btns_calculation(
                new_counter, btns_pressed, new_buttons_distribution
            )

    def calculate_min_btn_pressed(self) -> None:
        # Initialize variables
        counter = tuple([0 for _ in self.target_counter])
        btns_pressed = 0

        # Start recursion
        self._recursion_btns_calculation(counter, btns_pressed, self.joltage_buttons)


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> list[MachineJoltage]:
    """Avoiding light diagram"""
    machines: list[MachineJoltage] = []
    for line in file_content:
        _, *raw_schematics, raw_requirements = line.split()

        # Transform joltage requirements
        joltage_requirements = eval("(" + raw_requirements[1:-1] + ")")

        # Transform schematics to binary vectors
        buttons_schematic = []
        for str_schematic in raw_schematics:
            scheme = eval(str_schematic)
            if type(scheme) is int:
                scheme = tuple([scheme])  # special case for only 1 element in tuple
            buttons_schematic.append(scheme)

        # Store machine data
        machines.append(MachineJoltage(buttons_schematic, joltage_requirements))

    return machines


def solve_02(data: list[MachineJoltage]) -> int:
    count = 0
    for machine in data:
        machine.calculate_min_btn_pressed()
        count += machine.min_btn_pressed
    return count


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the example 1 is {solution}")
    # file_content = read_data(INPUT_FILE_PATH / "input.txt")
    # data = parse_input(file_content)
    # solution = solve_02(data)
    # print(f"The solution of the part 2 is {solution}")


if __name__ == "__main__":
    main()
