def create_sections(
    separation_points: list[int], max_value: int
) -> list[tuple[int, int]]:
    ini = -1
    sections = []
    for point in separation_points:
        sections.append((ini, point))
        ini = point
    sections.append((ini, max_value + 1))

    return sections


def classify_between_sections(
    sections: list[tuple[int, int]], all_values: list[int]
) -> dict[tuple[int, int], list[int]]:
    filled_sections = {}
    for section in sections:
        values = [val for val in all_values if val > section[0] and val < section[1]]
        filled_sections.update({section: values})

    return filled_sections


def reorder_section_values(
    section: tuple[int, int], values: list[int], inverse: bool = False
) -> list[int]:
    new_values = []
    if not inverse:
        occupied_pos = section[0]
        for _ in values:
            occupied_pos += 1  # Next position to be occupied
            new_values.append(occupied_pos)
    else:
        occupied_pos = section[1]
        for _ in values:
            occupied_pos -= 1  # Next position to be occupied
            new_values.append(occupied_pos)

    return new_values


def tilt_platform(
    round_rocks: list[int],
    cube_rocks: list[int],
    max_position: int,
    inverse_order: bool = False,
) -> list[int]:
    new_round_rocks = []
    sections = create_sections(cube_rocks, max_position)
    filled_sections = classify_between_sections(sections, round_rocks)
    for section, rock_coords in filled_sections.items():
        new_rock_coords = reorder_section_values(
            section, rock_coords, inverse=inverse_order
        )
        new_round_rocks.extend(new_rock_coords)

    return new_round_rocks
