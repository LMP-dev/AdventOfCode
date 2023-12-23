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
