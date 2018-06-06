#include <stdio.h>
#include <stdbool.h>

#define N 9

void print_sudoku(int grid[N][N]) {
    for (int i = 0; i < N; ++i) {
        if (i % 3 == 0 && i != 0) {
            puts("------+-------+------");
        }
        for (int j = 0; j < N; ++j) {
            if (j % 3 == 0 && j != 0) {
                printf("| ");
            }
            if (grid[i][j] == 0) {
                putchar('.');
            } else {
                printf("%d", grid[i][j]);
            }
            putchar(j == N-1 ? '\n' : ' ');
        }
    }
}

bool used_in_row(int grid[N][N], int row, int num) {
    for (int col = 0; col < N; ++col) {
        if (grid[row][col] == num) return true;
    }
    return false;
}

bool used_in_col(int grid[N][N], int col, int num) {
    for (int row = 0; row < N; ++row) {
        if (grid[row][col] == num) return true;
    }
    return false;
}

bool used_in_box(int grid[N][N], int box_start_row, int box_start_col, int num) {
    for (int r = 0; r < 3; ++r) {
        for (int c = 0; c < 3; ++c) {
            if (grid[r + box_start_row][c + box_start_col] == num) return true;
        }
    }
    return false;
}

bool is_valid(int grid[N][N], int row, int col, int num) {
    return !used_in_row(grid, row, num) && !used_in_col(grid, col, num) &&
           !used_in_box(grid, row - row % 3, col - col % 3, num);
}

bool find_empty_location(int grid[N][N], int *row, int *col) {
    for (*row = 0; *row < N; ++(*row)) {
        for (*col = 0; *col < N; ++(*col)) {
            if (grid[*row][*col] == 0) {
                return true;
            }
        }
    }
    return false;
}

bool solve_sudoku(int grid[N][N]) {
    int row, col;
    if (!find_empty_location(grid, &row, &col)) {
        return true;
    }

    bool candidates[N+1];
    for (int i = 1; i <= N; i++) candidates[i] = true;

    for (int j = 0; j < N; j++) {
        int v = grid[row][j];
        if (v != 0) candidates[v] = false;
    }
    for (int i = 0; i < N; i++) {
        int v = grid[i][col];
        if (v != 0) candidates[v] = false;
    }
    int br = row - row % 3;
    int bc = col - col % 3;
    for (int i = br; i < br + 3; i++) {
        for (int j = bc; j < bc + 3; j++) {
            int v = grid[i][j];
            if (v != 0) candidates[v] = false;
        }
    }

    for (int num = 1; num <= N; ++num) {
        if (candidates[num]) {
            grid[row][col] = num;
            if (solve_sudoku(grid)) return true;
            grid[row][col] = 0;
        }
    }

    return false;
}

int count_unsolved(int grid[N][N]) {
    int cnt = 0;
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            if (grid[i][j] == 0) cnt++;
        }
    }
    return cnt;
}

bool validate_sudoku(int grid[N][N]) {
    bool present[N+1];
    for (int i = 0; i < N; ++i) {
        for (int v = 1; v <= N; ++v) present[v] = false;
        for (int j = 0; j < N; ++j) {
            int val = grid[i][j];
            if (val != 0) {
                if (present[val]) return false;
                present[val] = true;
            }
        }

        for (int v = 1; v <= N; ++v) present[v] = false;
        for (int j = 0; j < N; ++j) {
            int val = grid[j][i];
            if (val != 0) {
                if (present[val]) return false;
                present[val] = true;
            }
        }
    }

    for (int br = 0; br < N; br += 3) {
        for (int bc = 0; bc < N; bc += 3) {
            for (int v = 1; v <= N; ++v) present[v] = false;
            for (int r = 0; r < 3; ++r) {
                for (int c = 0; c < 3; ++c) {
                    int val = grid[br+r][bc+c];
                    if (val != 0) {
                        if (present[val]) return false;
                        present[val] = true;
                    }
                }
            }
        }
    }
    return true;
}

int main(void) {
    int grid[N][N] = {
        {3,0,0,0,0,0,0,0,0},
        {0,0,0,0,3,8,0,0,9},
        {0,7,0,2,6,0,0,0,5},
        {0,5,0,0,0,0,0,3,1},
        {8,0,3,0,9,0,7,0,6},
        {2,6,0,0,0,0,0,9,0},
        {5,0,0,0,2,6,0,8,0},
        {6,0,0,1,5,0,0,0,0},
        {0,0,0,0,0,0,0,0,3}
    };

    puts("Initial Sudoku:");
    print_sudoku(grid);
    printf("Unsolved cells: %d\n", count_unsolved(grid));

    if (!validate_sudoku(grid)) {
        puts("Invalid initial Sudoku.");
        return 1;
    }

    bool solved = solve_sudoku(grid);
    puts(solved ? "\nSolved:" : "\nNo solution found");
    print_sudoku(grid);
    printf("Unsolved cells after: %d\n", count_unsolved(grid));

    return solved ? 0 : 2;
}
