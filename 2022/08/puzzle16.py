from pathlib import Path

import numpy as np

INPUT_FILE = Path(__file__).parent / "input.txt"
# INPUT_FILE = Path(__file__).parent / "test_input.txt"


class TreeGrid:
    """0 not visible, 1 visible"""

    def __init__(self, grid: np.ndarray) -> None:
        self.grid = grid
        self.rows, self.cols = grid.shape
        self.highest_scenic_score = 0

    def _visible_trees(self, ordered_array: np.ndarray, tree_height: int) -> int:
        """ordered_array must start with the tree which tree_height is given."""
        visible_trees = 0
        visible_array = ordered_array - tree_height
        for tree in visible_array[1:]:
            visible_trees += 1
            if not tree < 0:
                break
        return visible_trees

    def calculate_scenic_score(self) -> None:
        for i, row in enumerate(self.grid):
            for j, tree in enumerate(row):
                left_trees = self.grid[i, : j + 1]
                right_trees = self.grid[i, j:]
                top_trees = self.grid[: i + 1, j]
                bottom_trees = self.grid[i:, j]
                num_trees_left = self._visible_trees(left_trees[::-1], tree)
                num_trees_right = self._visible_trees(right_trees, tree)
                num_trees_top = self._visible_trees(top_trees[::-1], tree)
                num_trees_bottom = self._visible_trees(bottom_trees, tree)

                senic_score = (
                    num_trees_left * num_trees_right * num_trees_top * num_trees_bottom
                )
                if senic_score > self.highest_scenic_score:
                    self.highest_scenic_score = senic_score


def create_tree_grid_matrix(input_file: Path) -> np.ndarray:
    with open(input_file, "r") as file:
        grid = list()
        for line in file:
            row = [int(char) for char in line.strip()]
            grid.append(row)
    return np.array(grid)


def main() -> None:
    grid = create_tree_grid_matrix(INPUT_FILE)
    tree_grid = TreeGrid(grid)
    tree_grid.calculate_scenic_score()
    print(tree_grid.highest_scenic_score)


if __name__ == "__main__":
    main()
