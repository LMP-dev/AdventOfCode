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
