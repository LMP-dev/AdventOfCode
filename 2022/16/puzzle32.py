import re
from pathlib import Path
import time
from functools import cache

start = time.time()

INPUT_FILE = Path(__file__).parent / "input.txt"
# INPUT_FILE = Path(__file__).parent / "test_input.txt"

# As all solutions are being chequed, intead of paralel, the elephant will be in series:
@cache  # to use cache the function need hashable arguments!
def solve(
    position: str, time: int, opened: frozenset, elephnat_not_started: bool
) -> int:
    """Finds the maximum pressure"""
    # Stop recurrence
    if time == 0:
        if elephnat_not_started:
            return solve("AA", 26, opened, False)
        return 0

    # Solve for moving to next valves
    pressure = max(
        solve(neigh, time - 1, opened, elephnat_not_started)
        for neigh in neighbours[position]
    )

    # Only check for positive flow_rates and not opened valves
    if flow_rates[position] > 0 and position not in opened:
        unfrozen_opened = set(opened)
        unfrozen_opened.add(position)
        # Open if more pressure than advancing
        pressure = max(
            pressure,
            (time - 1) * flow_rates[position]
            + solve(
                position, time - 1, frozenset(unfrozen_opened), elephnat_not_started
            ),
        )
    return pressure


def read_valves(file_path: Path) -> tuple[dict]:
    """Returns a dictionary with each valve flow rate and connections"""
    flow_rates = dict()
    neighbours = dict()
    with open(file_path, "r") as file:
        for line in file:
            # Parsing
            valve_sentence, leads_sentence = line.strip().split(";")
            valve_part, flow_rate = valve_sentence.split("=")
            valve = re.findall("([A-Z][A-Z])+", valve_part)[0]
            other_valves = re.findall("([A-Z][A-Z])+", leads_sentence)
            # Fill dictionaris
            flow_rates[valve] = int(flow_rate)
            neighbours[valve] = other_valves
    return flow_rates, neighbours


flow_rates, neighbours = read_valves(INPUT_FILE)
total_pressure = solve("AA", 26, frozenset(), True)
print(total_pressure)
print(f"--- {(time.time() - start) * 1000} ms ---")
