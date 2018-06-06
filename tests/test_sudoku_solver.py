import pytest
from sudoku_solver import validate_sudoku, solve_sudoku, count_unsolved

VALID_GRID = [
    [5,3,0,0,7,0,0,0,0],
    [6,0,0,1,9,5,0,0,0],
    [0,9,8,0,0,0,0,6,0],
    [8,0,0,0,6,0,0,0,3],
    [4,0,0,8,0,3,0,0,1],
    [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0],
    [0,0,0,4,1,9,0,0,5],
    [0,0,0,0,8,0,0,7,9],
]

EXPECTED_SOLVED = [
    [5,3,4,6,7,8,9,1,2],
    [6,7,2,1,9,5,3,4,8],
    [1,9,8,3,4,2,5,6,7],
    [8,5,9,7,6,1,4,2,3],
    [4,2,6,8,5,3,7,9,1],
    [7,1,3,9,2,4,8,5,6],
    [9,6,1,5,3,7,2,8,4],
    [2,8,7,4,1,9,6,3,5],
    [3,4,5,2,8,6,1,7,9],
]

INVALID_ROW = [
    [5,5,1,0,0,0,0,0,0],
] + [[0]*9 for _ in range(8)]

INVALID_COL = [
    [5,0,0,0,0,0,0,0,0],
    [5,0,0,0,0,0,0,0,0],
] + [[0]*9 for _ in range(7)]

INVALID_BOX = [
    [1,2,3,0,0,0,0,0,0],
    [4,1,6,0,0,0,0,0,0],
    [7,8,9,0,0,0,0,0,0],
] + [[0]*9 for _ in range(6)]


def test_validate_sudoku_valid():
    assert validate_sudoku(VALID_GRID)


def test_validate_sudoku_invalid_row():
    assert not validate_sudoku(INVALID_ROW)


def test_validate_sudoku_invalid_col():
    assert not validate_sudoku(INVALID_COL)


def test_validate_sudoku_invalid_box():
    assert not validate_sudoku(INVALID_BOX)


def test_solve_sudoku_completes_with_valid_solution():
    grid = [row.copy() for row in VALID_GRID]
    assert solve_sudoku(grid)
    assert grid == EXPECTED_SOLVED


def test_count_unsolved():
    assert count_unsolved(VALID_GRID) == 51
