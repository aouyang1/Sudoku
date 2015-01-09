"""
SudokuTable class with the fields:

- 'fname', filename of input csv file
- 'table', Sudoku table
- 'unmarked', unmarked structure containing location of unmarked cells and possibilities
- 'error_status', identifies if current Sudoku table has any violations

functions:

- 'initialize_unmarked', set the potential values for each unmarked cell
- 'check_for_error', check to see if any zone, row, or column has more than one occurrence of a value
- 'fill_and_update_table', fill the table with unmarked cells having only a single possibility and clean
                           zone, row, and columns
- 'copy_sudoku', copy the contents of a sudoku class to another sudoku class
- 'setup_brute_force', setup the brute force approach when all other strategies have been exhausted
"""

import numpy as np
from unmarked import Unmarked


class SudokuTable:

    ZONE_SIZE = 3

    def __init__(self, fname="",
                 table=np.zeros(0),
                 unmarked_table_idx=np.zeros(0)):
        self.fname = fname
        self.table = table
        self.unmarked = Unmarked(table_idx=unmarked_table_idx)
        self.error_status = False

    def initialize_unmarked(self):
        # set the potential values in each unmarked cell

        cnt = 0
        for zone_row, zone_col in zip(self.unmarked.get_zone_row(), self.unmarked.get_zone_col()):

            table_row = self.unmarked.get_table_row()[cnt]
            table_col = self.unmarked.get_table_col()[cnt]

            # get current zone, row, col for selected cell
            curr_zone = self.table[zone_row*self.ZONE_SIZE:(zone_row+1)*self.ZONE_SIZE,
                                   zone_col*self.ZONE_SIZE:(zone_col+1)*self.ZONE_SIZE]
            curr_row = self.table[table_row, :]
            curr_col = self.table[:, table_col]

            # gather numbers
            numbers_used_in_zone = curr_zone[curr_zone.nonzero()]
            numbers_used_in_row = curr_row[curr_row.nonzero()]
            numbers_used_in_col = curr_col[curr_col.nonzero()]

            # find all numbers that have been used in zone, row, and column
            numbers_used = np.unique(np.concatenate([numbers_used_in_zone,
                                                     numbers_used_in_row,
                                                     numbers_used_in_col]))

            # get potential values in selected cell
            val = np.array(list(set(numbers_used) ^ set(np.arange(1, 10))))

            # set possible values for each cell
            self.unmarked.possibilities[cnt, :(len(val))] = val

            # update unmarked count
            cnt += 1

    def check_for_error(self):
        # iterate through all rows, columns, and zone to ensure all numbers occurs only once
        for row in range(self.table.shape[0]):
            curr_table_row = self.table[row, :]

            # get a count for each number 1-9
            num_occurrences = np.bincount(curr_table_row[curr_table_row.nonzero()].astype(int))
            if np.any(num_occurrences > 1):
                self.error_status = True
                break

        if not self.error_status:
            for col in range(self.table.shape[1]):
                curr_table_col = self.table[:, col]

                # get a count for each number 1-9
                num_occurrences = np.bincount(curr_table_col[curr_table_col.nonzero()].astype(int))
                if np.any(num_occurrences > 1):
                    self.error_status = True
                    break

        if not self.error_status:
            if self.unmarked.possibilities.shape[0] != 0:
                if np.any(np.sum(self.unmarked.possibilities == 0, axis=1) == self.table.shape[0]):
                    self.error_status = True

    def fill_and_update_table(self, rows_with_only_one):
        # unmarked cells with only one possibility are removed and table is filled with the corresponding value.
        # possibilities in zone, column, and row are also removed
        unmarked_single = self.unmarked.get_single_possibilities(rows_with_only_one)

        # replace table values with final value
        table_coor_with_one = self.unmarked.table_idx[rows_with_only_one, :]
        self.table[table_coor_with_one[:, 0], table_coor_with_one[:, 1]] = unmarked_single

        # remove possible values in zone, row, and column with found values
        zone_coor_with_one = self.unmarked.zone_idx[rows_with_only_one, :]
        self.unmarked.clean_value_in_scope(unmarked_single, zone_coor_with_one, scope="zone")
        self.unmarked.clean_value_in_scope(unmarked_single, table_coor_with_one[:, 0], scope="row")
        self.unmarked.clean_value_in_scope(unmarked_single, table_coor_with_one[:, 1], scope="col")

    def copy_sudoku(self, SudokuClass):
        # copy the table, and unmarked class to another sudoku class
        self.table = SudokuClass.table.copy()
        self.unmarked.table_idx = SudokuClass.unmarked.table_idx.copy()
        self.unmarked.zone_idx = SudokuClass.unmarked.zone_idx.copy()
        self.unmarked.possibilities = SudokuClass.unmarked.possibilities.copy()
        self.unmarked.num = SudokuClass.unmarked.num

    def setup_brute_force(self):
        # set up the start of brute force strategy by setting only one value to the first unmarked cell
        first_row_unmarked_possibilities = self.unmarked.possibilities[0, :]
        val_loc = first_row_unmarked_possibilities.nonzero()
        first_val = first_row_unmarked_possibilities[val_loc][0]
        self.unmarked.possibilities[0, :] = np.zeros(self.ZONE_SIZE**2)
        self.unmarked.possibilities[0, val_loc[0][0]] = first_val
