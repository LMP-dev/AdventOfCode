from pathlib import Path

import numpy as np

INPUT_FILE = Path(__file__).parent / "input.txt"
# INPUT_FILE = Path(__file__).parent / "test_input.txt"


def parse_input(file_path: Path) -> np.ndarray:
    grid = list()
    with open(file_path, "r") as file:
        for i, line in enumerate(file):
            row = list()
            for j, char in enumerate(line.strip()):
                if char == "S":
                    start = (i, j)
                    row.append(1)
                elif char == "E":
                    end = (i, j)
                    row.append(26)  # z value
                else:
                    val = ord(char) - 96  # ord("a") = 97
                    row.append(val)
            grid.append(row)
    return grid, start, end


def find_all_neighbours(pos: tuple[int], shape: tuple[int]) -> list[tuple[int]]:
    neighbours = list()
    if not pos[0] == 0:
        north = (pos[0] - 1, pos[1])
        neighbours.append(north)
    if not pos[1] == shape[1] - 1:
        east = (pos[0], pos[1] + 1)
        neighbours.append(east)
    if not pos[0] == shape[0] - 1:
        sud = (pos[0] + 1, pos[1])
        neighbours.append(sud)
    if not pos[1] == 0:
        west = (pos[0], pos[1] - 1)
        neighbours.append(west)
    return neighbours


def filter_feasible_neighbours_var(
    height_grid: np.ndarray, current_pos: tuple[int], visited: np.ndarray
) -> list[tuple[int]]:
    feasible_neighbours = list()
    all_neighbours = find_all_neighbours(current_pos, height_grid.shape)
    current_heigh = height_grid[current_pos]
    for neigh in all_neighbours:
        if height_grid[neigh] >= current_heigh - 1 and not visited[neigh]:
            feasible_neighbours.append(neigh)
    return feasible_neighbours


def dijkstra_variation(heights: np.ndarray, start: tuple[int]):
    visited = np.zeros(heights.shape, dtype=bool)
    visited[start] = True
    distances = np.ones(heights.shape) * np.inf
    distances[start] = 26
    backtrack = np.zeros(heights.shape, dtype=("i,i"))
    finished = False
    while not finished:
        # take next lowest distance node
        nodes = np.where(distances == np.amin(distances))
        node = (nodes[0][0], nodes[1][0])
        if heights[node] == 1:
            finished = True
            end = node
            break
        # Find neighbours node
        neighbours = filter_feasible_neighbours_var(heights, node, visited)
        for neigh in neighbours:
            distances[neigh] = heights[neigh] + distances[node]
            backtrack[neigh] = node
            visited[neigh] = True
        distances[node] = np.inf
    count = 0
    last_node = end
    counting = True
    while counting:
        last_node = tuple(backtrack[last_node])
        count += 1
        if last_node == start:
            break
    return count


def main() -> None:
    grid, start, end = parse_input(INPUT_FILE)
    height_grid = np.array(grid)
    print(dijkstra_variation(height_grid, end))


if __name__ == "__main__":
    main()
