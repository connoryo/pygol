from copy import deepcopy
from random import random
from typing import List, Optional


class Board:
    """
    Represents a Game of Life board. The board can be initialized with a specific width and height,
    and can optionally have wrap-around behavior for edge cells.
    """

    def __init__(self, width: Optional[int] = 10, height: Optional[int] = 10, wrap_around: Optional[bool] = False):
        """
        Initializes the board with the given width, height, and wrap-around option.
        The board is initially set to a 'dead' state (all 0s).

        Args:
            width (Optional[int]): The width of the board. Defaults to 10.
            height (Optional[int]): The height of the board. Defaults to 10.
            wrap_around (Optional[bool]): Whether the board wraps around at the edges. Defaults to False.
        """
        self.dead_state(width, height)
        self.wrap_around = wrap_around

    def __repr__(self) -> str:
        """
        Returns a string representation of the current board state.
        Filled squares represent live cells and blank spaces represent dead cells.

        Returns:
            str: A string representation of the board.
        """
        result = ""

        # Add top of board
        result += '┌'
        for _ in range(2 * self.width):
            result += '─'
        result += '┐\n'

        # Add sides of board + board contents
        for i in range(self.height):
            result += '│'
            for j in range(self.width):
                result += '██' if self.board[i][j] == 1 else '  '
            result += '│\n'

        # Add bottom of board
        result += '└'
        for _ in range(2 * self.width):
            result += '─'
        result += '┘\n'
        return result

    def render(self):
        """
        Prints the current board state to the console.
        """
        print(self)

    def load_board_from_file(self, filename: str):
        """
        Loads a board state from a file where each line represents a row of the board.
        Cells are represented as 0 (dead) or 1 (alive).

        Args:
            filename (str): The name of the file to load the board state from.

        Returns:
            self: The board with the new state set.
        """
        with open(filename, "r") as infile:
            new_board_state = []
            for line in infile:
                new_board_state.append([int(char) for char in line if char != '\n'])

        return self.set_state(new_board_state)

    def set_state(self, new_board: List[List[int]]):
        """
        Sets the current state of the board with a new 2D list of integers representing live (1) or dead (0) cells.

        Args:
            new_board (List[List[int]]): A 2D list representing the new board state.

        Raises:
            ValueError: If the desired board state is invalid

        Returns:
            self: The board with the updated state.
        """
        self.height = len(new_board)
        if self.height < 1:
            raise ValueError("State cannot be empty!")

        self.width = len(new_board[0])
        if any(len(x) != self.width for x in new_board):
            raise ValueError("All rows of the board must be equal length!")

        for row in new_board:
            if any(x not in [0, 1] for x in row):
                raise ValueError("All cells must be either 0 or 1!")

        self.board = new_board
        return self

    def get_state(self) -> List[List[int]]:
        """
        Returns the current state of the board as a 2D list of integers.

        Returns:
            List[List[int]]: The current board state.
        """
        return self.board

    def dead_state(self, width: Optional[int] = None, height: Optional[int] = None):
        """
        Sets the board state to all dead cells.

        Args:
            width (Optional[int]): The width of the board. Defaults to the board's current width.
            height (Optional[int]): The height of the board. Defaults to the board's current height.

        Returns:
            self: The board with all cells set to dead.
        """
        return self.random_state(width, height, dead_cell_proportion=1.0)

    def random_state(self, width: Optional[int] = None, height: Optional[int] = None, dead_cell_proportion: float = 0.5):
        """
        Initializes the board with random live or dead cells. The probability of a cell being dead is determined
        by the dead_cell_proportion.

        Args:
            width (int): The width of the board. Defaults to the board's current width.
            height (int): The height of the board. Defaults to the board's current height.
            dead_cell_proportion (float): The proportion of cells that are dead. Defaults to 0.5.

        Returns:
            self: The board with a random state.
        """
        if width:
            self.width = width
        if height:
            self.height = height
        self.board = []
        for _ in range(self.height):
            row = []
            for _ in range(self.width):
                row.append(0 if random() < dead_cell_proportion else 1)
            self.board.append(row)
        return self

    def _count_alive_neighbors(self, i: int, j: int) -> int:
        """
        Counts the number of live neighbors for a given cell at position (i, j).

        Args:
            i (int): The row index of the cell.
            j (int): The column index of the cell.

        Returns:
            int: The number of live neighbors around the cell.
        """
        n_neighbors_alive = 0
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if x == 0 and y == 0:
                    continue
                if not self.wrap_around:
                    if (i + x) < 0 or (i + x) >= self.height:
                        continue
                    if (j + y) < 0 or (j + y) >= self.width:
                        continue
                if self.board[(i + x) % self.height][(j + y) % self.width] == 1:
                    n_neighbors_alive += 1
        return n_neighbors_alive

    def iterate_state(self):
        """
        Advances the board state by one generation according to the rules of Conway's Game of Life.
        Live cells may die due to underpopulation or overpopulation, and dead cells may come alive by reproduction.

        Returns:
            self: The board with the updated state.
        """
        new_state = deepcopy(self.board)
        for i in range(self.height):
            for j in range(self.width):
                n_neighbors_alive = self._count_alive_neighbors(i, j)

                # Implement game rules here
                if self.board[i][j] == 1 and n_neighbors_alive < 2:
                    new_state[i][j] = 0  # Any live cell with 0 or 1 live neighbors becomes dead, because of underpopulation
                elif new_state[i][j] == 1 and n_neighbors_alive in [2, 3]:
                    continue  # Any live cell with 2 or 3 live neighbors stays alive, because its neighborhood is just right
                elif self.board[i][j] == 1 and n_neighbors_alive > 3:
                    new_state[i][j] = 0  # Any live cell with more than 3 live neighbors becomes dead, because of overpopulation
                elif self.board[i][j] == 0 and n_neighbors_alive == 3:
                    new_state[i][j] = 1  # Any dead cell with exactly 3 live neighbors becomes alive, by reproduction
                else:
                    continue
        return self.set_state(new_state)
