# Standard library
from pathlib import Path
import math
import copy
from typing import TypeVar, Iterator


INPUT_FILE_PATH = Path(__file__).parent

T = TypeVar("T")


def _combos(
    elements: Iterator[tuple[T, int]], start_idx: int, length: int
) -> Iterator[tuple[T, ...]]:
    """
    Copied from StackOverflow. It creates combinations with repetition and max repetitions allowed.
    n = length (number of elements in the combination)
    r = elements[i][0] types of elements to select
    max r = elements[i][1] maximum repetitions of this type in final combination
    """
    # ignore elements before start_idx
    for i in range(start_idx, len(elements)):
        elem, max_count = elements[i]
        if max_count == 0:
            continue
        # base case: only one element needed
        if length == 1:
            yield (elem,)
        else:
            # need more than one elem: mutate the list and recurse
            # Reduce max count of element selected
            elements[i] = (elem, max_count - 1)
            # when we recurse, we ignore elements before this one
            # this ensures we find combinations, not permutations
            for combo in _combos(elements, i, length - 1):
                yield (elem,) + combo
            # fix the original list
            elements[i] = (elem, max_count)


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
    def _increase_counter(
        counter: tuple[int, ...], btns_combination: tuple[tuple[int, ...]]
    ) -> tuple[int, ...]:
        temp_counter = list(counter)
        for button in btns_combination:
            for index in button:
                temp_counter[index] += 1
        return tuple(temp_counter)

    def _select_next_counter_to_fill(
        self, counter: tuple[int, ...], buttons: list[list[dict[tuple[int, ...], int]]]
    ) -> int:
        # Calculate number of types (buttons) for each counter
        num_buttons = [len(btn_types) for btn_types in buttons]

        diff_counter = tuple(
            [target - count for target, count in zip(self.target_counter, counter)]
        )
        if any(diff < 0 for diff in diff_counter):
            raise Exception(
                "Counter have exceeded the target counter! Something went wrong in recursion function!"
            )  # Check if inputs are correct

        try:
            # Identify counter with only 1 button to click
            index = num_buttons.index(1)
            # Guard to check counter is not at max value
            if diff_counter[index] == 0:
                raise ValueError
        except ValueError:
            # Identify counter with only 2 buttons to click
            index = num_buttons.index(2)
            # Guard to check counter is not at max value
            if diff_counter[index] == 0:
                raise ValueError
        except ValueError:
            # If not select min diff column not empty
            min_counter = min(
                diff for diff in diff_counter if diff > 0
            )  # Only counters not at target
            index = list(diff_counter).index(min_counter)

        return index

    def _allowed_combinations(
        self,
        index: int,
        counter: tuple[int, ...],
        buttons: dict[tuple[int, ...], int],
    ) -> list[tuple[tuple[int, ...], ...]]:
        # Calculate number of buttons to click to push counter to target
        num_btns_to_click = self.target_counter[index] - counter[index]

        # Adapt buttons available to select
        available_buttons = [(btn, max_rep) for btn, max_rep in buttons.items()]

        # Calculate combinations
        return list(_combos(available_buttons, 0, num_btns_to_click))

    def _remove_buttons_used(
        self,
        index: int,
        buttons_distribution: list[list[dict[tuple[int, ...], int]]],
    ) -> list[list[dict[tuple[int, ...], int]]]:
        # Copy original distribution
        new_distribution = copy.deepcopy(buttons_distribution)

        for button in buttons_distribution[index]:
            for index in button:
                del new_distribution[index][button]

        return new_distribution

    def _recursion_btns_calculation(
        self,
        counter: tuple[int, ...],
        btns_pressed: int,
        buttons_distribution: list[list[dict[tuple[int, ...], int]]],
    ):
        # Reduce by MUST click buttons
        # TODO

        # Select next counter to fill
        index = self._select_next_counter_to_fill(counter, buttons_distribution)

        # Create allowed combinations considering the max repetition of elements
        allowed_btns_combinations = self._allowed_combinations(
            index, counter, buttons_distribution[index]
        )

        # Loop through all options
        for btns_combination in allowed_btns_combinations:
            # Increase btns_pressed count
            new_btns_pressed = btns_pressed + len(btns_combination)

            # Increase counter
            new_counter = self._increase_counter(counter, btns_combination)

            # Guard clauses to stop recursion
            if any(
                now > target for now, target in zip(new_counter, self.target_counter)
            ):
                return
            if new_counter == self.target_counter:
                if new_btns_pressed < self.min_btn_pressed:
                    self.min_btn_pressed = new_btns_pressed
                return

            # Remove buttons used from buttons_distribution
            new_buttons_distribution = self._remove_buttons_used(
                index, buttons_distribution
            )

            # Call again function
            self._recursion_btns_calculation(
                new_counter, new_btns_pressed, new_buttons_distribution
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
    for i, machine in enumerate(data):
        machine.calculate_min_btn_pressed()
        print(f"For machine in line {i+1} the count is: {machine.min_btn_pressed}")
        count += machine.min_btn_pressed
    return count


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the example 1 is {solution}")  # Solution 33
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the part 2 is {solution}")  # Solution


if __name__ == "__main__":
    main()
