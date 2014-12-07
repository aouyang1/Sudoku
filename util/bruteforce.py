"""
BruteForce class with the fields:

- 'status', boolean representing whether brute force approach is in effect
- 'possibilities_cnt', index to iterate through all possibilities in remaining unmarked cells
- 'sudoku', sudoku table which will be copied from the workind sudoku table after brute force is put into effect
"""

from util.sudokutable import SudokuTable


class BruteForce:

    def __init__(self):
        self.status = False
        self.possibilities_cnt = 0
        self.sudoku = SudokuTable()

