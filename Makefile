.PHONY: all python c test clean

all: python c

python:
	python3 sudoku_solver.py

c:
	gcc -std=c11 -O2 sudoku_solver.c -o sudoku_solver
	./sudoku_solver

test:
	pytest -q

clean:
	rm -f sudoku_solver
