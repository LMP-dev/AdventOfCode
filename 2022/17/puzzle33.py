from pathlib import Path
import time


INPUT_FILE = Path(__file__).parent / "input.txt"
# INPUT_FILE = Path(__file__).parent / "test_input.txt"  # Solution = 3068

"""
Chamber, 7 units wide (col 0 and 8 are walls):
|.......|
|.......|
+-------+

Rocks:
####   0011110

.#.    0001000
###    0011100
.#.    0001000

..#    0000100
..#    0000100
###    0011100

#      0010000
#      0010000
#      0010000
#      0010000

##     0011000
##     0011000

< push left
> push right 

3 units above highest rock (or floor)
"""

ROCKS = [
    [(1, 3), (1, 4), (1, 5), (1, 6)],  # ~ rock
    [(1, 4), (2, 3), (2, 4), (2, 5), (3, 4)],  # + rock
    [(1, 3), (1, 4), (1, 5), (2, 5), (3, 5)],  # L rock
    [(1, 3), (2, 3), (3, 3), (4, 3)],  # | rock
    [(1, 3), (1, 4), (2, 3), (2, 4)],  # o rock
]

JET_MOVEMENT = {"<": -1, ">": 1}


def parse_input(file_path: Path) -> list[str]:
    with open(file_path, "r") as file:
        jets = file.readlines()

    jet_line = jets[0].strip()
    return list(jet_line)


def jet_movement(
    rock: list[tuple[int]], jet: str, still_rocks: list[tuple[int]]
) -> list[tuple[int]]:
    """Move the rock left or right and checks if wall hit."""
    movement = JET_MOVEMENT[jet]
    new_rock = [(pos[0], pos[1] + movement) for pos in rock]
    if any(pos[1] < 1 or pos[1] > 7 or pos in still_rocks for pos in new_rock):
        return rock  # collision with walls or still rock
    return new_rock


def down_movement(
    rock: list[tuple[int]], still_rocks: list[tuple[int]]
) -> tuple[bool, list[tuple[int]]]:
    new_rock = [(pos[0] - 1, pos[1]) for pos in rock]
    if any(pos in still_rocks for pos in new_rock):
        return False, rock
    return True, new_rock


def sort_by_row(element: tuple[int]) -> int:
    return element[0]


def main():
    jets = parse_input(INPUT_FILE)
    running_rocks = 2022
    maximum_heigh = 0
    still_rocks = [
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 4),
        (0, 5),
        (0, 6),
        (0, 7),
    ]  # Initial floor

    for _ in range(running_rocks):
        no_pos_rock = ROCKS.pop(0)
        ROCKS.append(no_pos_rock)
        rock = [(pos[0] + maximum_heigh + 3, pos[1]) for pos in no_pos_rock]

        while True:
            jet = jets.pop(0)
            jets.append(jet)
            new_rock = jet_movement(rock, jet, still_rocks)
            moved, rock = down_movement(new_rock, still_rocks)
            if not moved:
                rock_max_heigh = max(pos[0] for pos in rock)
                if rock_max_heigh > maximum_heigh:
                    maximum_heigh = rock_max_heigh
                still_rocks.extend(rock)
                break
    still_rocks.sort(key=sort_by_row, reverse=True)
    print(still_rocks[0][0])


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"--- {(time.time() - start) * 1000} ms ---")
