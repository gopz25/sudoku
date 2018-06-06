"""Optimized Sudoku solver

This module reads a 9x9 Sudoku grid using 0 for empty cells,
solves it with backtracking and constraint checks, and prints results.
"""

from typing import List, Optional, Tuple

Grid = List[List[int]]
ALL_DIGITS = set(range(1, 10))


def print_sudoku(grid: Grid) -> None:
    for i, row in enumerate(grid):
        if i % 3 == 0 and i != 0:
            print("------+-------+------")
        print(" ".join(
            ("." if v == 0 else str(v)) + (" |" if j in (2, 5) else "")
            for j, v in enumerate(row)
        ))


def find_empty(grid: Grid) -> Optional[Tuple[int, int]]:
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return None


def is_valid(grid: Grid, row: int, col: int, value: int) -> bool:
    if value in grid[row]:
        return False

    if value in (grid[r][col] for r in range(9)):
        return False

    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if grid[r][c] == value:
                return False

    return True


def solve_sudoku(grid: Grid) -> bool:
    empty_pos = find_empty(grid)
    if empty_pos is None:
        return True

    row, col = empty_pos
    used = set(grid[row]) | {grid[r][col] for r in range(9)}

    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            used.add(grid[r][c])

    for candidate in ALL_DIGITS - used:
        if is_valid(grid, row, col, candidate):
            grid[row][col] = candidate
            if solve_sudoku(grid):
                return True
            grid[row][col] = 0

    return False


def count_unsolved(grid: Grid) -> int:
    return sum(1 for row in grid for value in row if value == 0)


def validate_sudoku(grid: Grid) -> bool:
    for i in range(9):
        row_vals = [v for v in grid[i] if v != 0]
        if len(row_vals) != len(set(row_vals)):
            return False

        col_vals = [grid[r][i] for r in range(9) if grid[r][i] != 0]
        if len(col_vals) != len(set(col_vals)):
            return False

    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            block = []
            for r in range(br, br + 3):
                for c in range(bc, bc + 3):
                    if grid[r][c] != 0:
                        block.append(grid[r][c])
            if len(block) != len(set(block)):
                return False

    return True


if __name__ == "__main__":
    matrix: Grid = [
        [3, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 3, 8, 0, 0, 9],
        [0, 7, 0, 2, 6, 0, 0, 0, 5],
        [0, 5, 0, 0, 0, 0, 0, 3, 1],
        [8, 0, 3, 0, 9, 0, 7, 0, 6],
        [2, 6, 0, 0, 0, 0, 0, 9, 0],
        [5, 0, 0, 0, 2, 6, 0, 8, 0],
        [6, 0, 0, 1, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 3],
    ]

    print("Initial Sudoku:")
    print_sudoku(matrix)
    print(f"Unsolved cells: {count_unsolved(matrix)}")

    if not validate_sudoku(matrix):
        raise ValueError("Provided Sudoku is invalid")

    solved = solve_sudoku(matrix)
    print("\nSolved:" if solved else "\nNo solution found")
    print_sudoku(matrix)
    print(f"Unsolved cells after: {count_unsolved(matrix)}")
