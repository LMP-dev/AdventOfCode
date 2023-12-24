from pathlib import Path

import numpy as np

INPUT_FILE = Path(__file__).parent / "input.txt"
# INPUT_FILE = Path(__file__).parent / "test_input.txt"
# INPUT_FILE = Path(__file__).parent / "own_test.txt"


class TreeGrid:
    """0 not visible, 1 visible"""

    def __init__(self, grid: np.ndarray) -> None:
        self.grid = grid
        self.rows, self.cols = grid.shape
        self.visibility = np.zeros(grid.shape)
        self._make_edge_visible()

    def _make_edge_visible(self) -> None:
        self.visibility[0, :] = np.ones(self.cols)  # top
        self.visibility[-1, :] = np.ones(self.cols)  # bottom
        self.visibility[:, 0] = np.ones(self.rows)  # left
        self.visibility[:, -1] = np.ones(self.rows)  # right

    def _left_visibility(self) -> None:
        vis_matrix = self.grid[1:-1, :]
        for i in range(self.cols - 1):
            vis_col = vis_matrix[:, i]
            visibility_step = np.atleast_2d(vis_col).T * np.ones(vis_matrix.shape)
            vis_matrix = vis_matrix - visibility_step
            vis_matrix = np.where(vis_matrix < 0, 0, vis_matrix)
            visible = vis_matrix[:, i + 1] > 0
            # Update visibility grid
            self.visibility[1:-1, i + 1][visible] = 1

    def _top_visibility(self) -> None:
        vis_matrix = self.grid[:, 1:-1]
        for i in range(self.rows - 1):
            vis_row = vis_matrix[i, :]
            visibility_step = np.atleast_2d(vis_row) * np.ones(vis_matrix.shape)
            vis_matrix = vis_matrix - visibility_step
            vis_matrix = np.where(vis_matrix < 0, 0, vis_matrix)
            visible = vis_matrix[i + 1, :] > 0
            # Update visibility grid
            self.visibility[i + 1, 1:-1][visible] = 1
            for index, element in enumerate(visible):
                if element == 1:
                    self.visibility[i + 1, index + 1] = 1

    def _right_visibility(self) -> None:
        vis_matrix = self.grid[1:-1, :]
        for i in range(self.cols - 1):
            vis_col = vis_matrix[:, -1 - i]
            visibility_step = np.atleast_2d(vis_col).T * np.ones(vis_matrix.shape)
            vis_matrix = vis_matrix - visibility_step
            vis_matrix = np.where(vis_matrix < 0, 0, vis_matrix)
            visible = vis_matrix[:, -2 - i] > 0
            # Update visibility grid
            self.visibility[1:-1, -2 - i][visible] = 1

    def _bottom_visibility(self) -> None:
        vis_matrix = self.grid[:, 1:-1]
        for i in range(self.rows - 1):
            vis_row = vis_matrix[-1 - i, :]
            visibility_step = np.atleast_2d(vis_row) * np.ones(vis_matrix.shape)
            vis_matrix = vis_matrix - visibility_step
            vis_matrix = np.where(vis_matrix < 0, 0, vis_matrix)
            visible = vis_matrix[-2 - i, :] > 0
            # Update visibility grid
            self.visibility[-2 - i, 1:-1][visible] = 1

    def calculate_visibility(self) -> np.ndarray:
        self._left_visibility()
        self._top_visibility()
        self._right_visibility()
        self._bottom_visibility()
        return self.visibility


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
    visibility_grid = tree_grid.calculate_visibility()
    print(visibility_grid.sum())


if __name__ == "__main__":
    main()
