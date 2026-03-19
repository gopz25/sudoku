"""Optimized Sudoku solver

This module reads a 9x9 Sudoku grid using 0 for empty cells,
solves it with backtracking and constraint checks, and prints results.
"""

import random
from typing import List, Optional, Tuple

Grid = List[List[int]]
ALL_DIGITS = set(range(1, 10))


RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"


def print_sudoku(grid: Grid) -> None:
    hborder_top = "╔" + "═══" * 3 + "╤" + "═══" * 3 + "╤" + "═══" * 3 + "╗"
    hborder_mid = "╠" + "═══" * 3 + "╪" + "═══" * 3 + "╪" + "═══" * 3 + "╣"
    hborder_bot = "╚" + "═══" * 3 + "╧" + "═══" * 3 + "╧" + "═══" * 3 + "╝"

    print("\n" + hborder_top)

    for i, row in enumerate(grid):
        line = "║"
        for j, v in enumerate(row):
            if v == 0:
                line += f" {DIM}.{RESET} "
            else:
                line += f" {BOLD}{GREEN}{v}{RESET} "

            if j in (2, 5):
                line += "│"
            elif j < 8:
                line += ""

        line += "║"
        print(line)

        if i in (2, 5):
            print(hborder_mid)

    print(hborder_bot)


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


def count_solutions(grid: Grid, limit: int = 2) -> int:
    """Return number of solutions up to limit."""
    empty_pos = find_empty(grid)
    if empty_pos is None:
        return 1

    row, col = empty_pos
    total = 0
    for candidate in range(1, 10):
        if is_valid(grid, row, col, candidate):
            grid[row][col] = candidate
            total += count_solutions(grid, limit)
            grid[row][col] = 0
            if total >= limit:
                return total
    return total


def solve_sudoku_random(grid: Grid) -> bool:
    empty_pos = find_empty(grid)
    if empty_pos is None:
        return True

    row, col = empty_pos
    candidates = list(ALL_DIGITS - set(grid[row]) - {grid[r][col] for r in range(9)} -
                      {grid[r][c] for r in range((row // 3) * 3, (row // 3) * 3 + 3)
                       for c in range((col // 3) * 3, (col // 3) * 3 + 3)})
    random.shuffle(candidates)

    for candidate in candidates:
        if is_valid(grid, row, col, candidate):
            grid[row][col] = candidate
            if solve_sudoku_random(grid):
                return True
            grid[row][col] = 0

    return False


def generate_puzzle(level: str = "med") -> tuple[Grid, Grid]:
    """Generate puzzle and solution with difficulty level and uniqueness check."""
    if level == "easy":
        removals = 40
    elif level in ("med", "medium"):
        removals = 50
    elif level == "hard":
        removals = 55
    else:
        raise ValueError("Level must be easy, med, or hard")

    while True:
        full = [[0] * 9 for _ in range(9)]
        solve_sudoku_random(full)
        solution = [row[:] for row in full]

        indices = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(indices)

        puzzle = [row[:] for row in full]
        for r, c in indices:
            if removals <= 0:
                break
            maybe = puzzle[r][c]
            if maybe == 0:
                continue
            puzzle[r][c] = 0

            tmp = [row[:] for row in puzzle]
            count = count_solutions(tmp, limit=2)
            if count != 1:
                puzzle[r][c] = maybe
            else:
                removals -= 1

        if count_solutions([row[:] for row in puzzle], limit=2) == 1:
            return puzzle, solution


def save_puzzle(path: str, grid: Grid) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for row in grid:
            f.write("".join(str(v) for v in row) + "\n")


def load_puzzle(path: str) -> Grid:
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    if len(lines) != 9:
        raise ValueError("Puzzle file must have 9 non-empty lines")
    grid = []
    for line in lines:
        line = line.replace(" ", "")
        if len(line) != 9 or any(ch not in "0123456789" for ch in line):
            raise ValueError("Each line must contain 9 digits (0-9)")
        grid.append([int(ch) for ch in line])
    return grid


def hint_cell(grid: Grid) -> tuple[int, int, set[int]] | None:
    # find first cell with smallest candidate set
    best = None
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                candidates = {n for n in range(1, 10) if is_valid(grid, i, j, n)}
                if not candidates:
                    return None
                if best is None or len(candidates) < len(best[2]):
                    best = (i, j, candidates)
    return best


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

    current_solution = None
    generated_puzzles = []
    generated_solutions = []
    puzzle_index = 0

    while True:
        print("\n" + BOLD + CYAN + "Sudoku Terminal UI" + RESET)
        print("1) Generate random puzzle")
        print("2) Generate 5 random puzzles (play later)")
        print("3) Solve default puzzle")
        print("4) Solve all generated puzzles")
        print("5) Show answer for current puzzle")
        print("6) Clear and exit")

        choice = input("Choose an option [1-6]: ").strip()

        if choice == "1":
            level = random.choice(["easy", "med", "hard"])
            matrix, current_solution = generate_puzzle(level)
            generated_puzzles = [matrix]
            generated_solutions = [current_solution]
            puzzle_index = 0
            print(YELLOW + f"Generated random puzzle (difficulty auto-selected: {level})" + RESET)

        elif choice == "2":
            generated_puzzles = []
            generated_solutions = []
            puzzle_difficulties = []
            for idx in range(5):
                level = random.choice(["easy", "med", "hard"])
                p, s = generate_puzzle(level)
                generated_puzzles.append(p)
                generated_solutions.append(s)
                puzzle_difficulties.append(level)

            puzzle_index = 0
            matrix = [row[:] for row in generated_puzzles[puzzle_index]]
            current_solution = generated_solutions[puzzle_index]
            print(YELLOW + "Generated 5 random puzzles (difficulty random per puzzle)." + RESET)

            for idx, puzzle in enumerate(generated_puzzles, start=1):
                level = puzzle_difficulties[idx - 1]
                print(f"\nPuzzle #{idx} (difficulty: {level}):")
                print_sudoku(puzzle)
            continue


        elif choice == "3":
            matrix = [
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
            solved_board = [row[:] for row in matrix]
            solved = solve_sudoku(solved_board)
            if solved:
                current_solution = [row[:] for row in solved_board]
                print("\nDefault puzzle solved:")
                print_sudoku(solved_board)
            else:
                print(YELLOW + "No solution found for default puzzle." + RESET)
            continue

        elif choice == "4":
            if not generated_puzzles:
                print(YELLOW + "No generated puzzles set. Use option 2 first." + RESET)
                continue
            print("\nSolving all generated puzzles...")
            for idx, puzzle in enumerate(generated_puzzles, start=1):
                solved = [row[:] for row in puzzle]
                if solve_sudoku(solved):
                    print(CYAN + f"\nPuzzle #{idx} solved:" + RESET)
                    print_sudoku(solved)
                else:
                    print(YELLOW + f"\nPuzzle #{idx} has no solution" + RESET)
            continue

        elif choice == "5":
            if current_solution is None:
                print(YELLOW + "No solved answer saved. Solve or generate a puzzle first." + RESET)
                continue
            confirm = input("Do you really want to show the answer? (y/n): ").strip().lower()
            if confirm != "y":
                continue
            print("\nSolution (answer):")
            print_sudoku([row[:] for row in current_solution])
            continue

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print(YELLOW + "Unknown option; choose 1-5." + RESET)
            continue

        # Display current puzzle after generation
        print("\nCurrent puzzle:")
        print_sudoku(matrix)
        print(f"Unsolved cells: {count_unsolved(matrix)}")


