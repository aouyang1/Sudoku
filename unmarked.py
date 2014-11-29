"""
Unmarked class with the fields:

- ZONE_SIZE, size of a zone in the sudoku table

function:

- 'convert_to_zone', takes a table index array (N by 2) and converts it to a zone index
- 'get_table_row', get the row indices of unmarked cells
- 'get_table_col', get the column indices of unmarked cells
- 'get_zone_row', get the zone row indices of unmarked cells
- 'get_zone_col', get the zone column indices of unmarked cells
- 'get_possibilities_index', get the row and column index of values in the possibilities matrix
- 'get_rows_with_n_possibilities', get the rows in the possibilities matrix with only n possibilities
- 'get_single_possibilities', get the value of cells with only one possibility
- 'get_double_possibilities', get the values of cells with only two possibilities
- 'get_table_rows_with_double', get the rows in the possibilities matrix with only two potential values
- 'get_table_cols_with_double', get the columns in the possibilities matrix with only two potential values
- 'get_zones_with_double', get the zone index of cells with only two potential values
- 'get_total_possibilities', get the total number of possibilities in remaining unmarked cells
- 'get_single_possibility', set a single possibility to a specific row in the possibilities matrix
- 'slice_class', keep specific unmarked cells of the table_idx, zone_idz, and possibilities matrix
- 'clean_value_in_scope', removes a value in all unmarked cells in a specified zone, column, or row
- 'clean_pairs_in_scope', remove a pair of values in all unmarked cells in a specified zone, column, or row
- 'clean_singles_in_scope', look for a single occurrence of a possibility within a specified zone, row or column
- 'solved', determine if there are no more unmarked cells signifying a solved sudoku
"""

import numpy as np


class Unmarked:

    ZONE_SIZE = 3

    def __init__(self, table_idx=np.zeros(0)):
        self.table_idx = table_idx
        self.zone_idx = self.convert_to_zone(table_idx)
        self.possibilities = np.zeros((table_idx.shape[0], self.ZONE_SIZE**2))
        self.num = table_idx.shape[0]

    def convert_to_zone(self, table_idx):
        # takes a table index array (N by 2) and converts it to a zone index
        zone_idx = np.floor(table_idx / self.ZONE_SIZE)
        return zone_idx

    def get_table_row(self):
        # get the row indices of unmarked cells
        table_row = self.table_idx[:, 0]
        return table_row

    def get_table_col(self):
        # get the column indices of unmarked cells
        table_col = self.table_idx[:, 1]
        return table_col

    def get_zone_row(self):
        # get the zone row indices of unmarked cells
        zone_row = self.zone_idx[:, 0]
        return zone_row

    def get_zone_col(self):
        # get the zone column indices of unmarked cells
        zone_col = self.zone_idx[:, 1]
        return zone_col

    def get_possibilities_index(self):
        # get the row and column index of values in the possibilities matrix
        row, col = self.possibilities.nonzero()
        return row, col

    def get_rows_with_n_possibilities(self, n):
        # get the rows in the possibilities matrix with only n possibilities
        row, col = self.get_possibilities_index()
        rows_with_only_two = np.where(np.bincount(row) == n)[0]
        return rows_with_only_two

    def get_single_possibilities(self, rows_with_single):
        # get the value of cells with only one possibility
        single = self.possibilities[rows_with_single, :]
        single = single[single.nonzero()]
        return single

    def get_double_possibilities(self, rows_with_double):
        # get the values of cells with only two possibilities
        double = self.possibilities[rows_with_double, :]
        double = double[double.nonzero()].reshape(rows_with_double.shape[0], 2)
        return double

    def get_table_rows_with_double(self, rows_with_double):
        # get the rows in the possibilities matrix with only two potential values
        rows_with_double = self.table_idx[rows_with_double, 0]
        return rows_with_double

    def get_table_cols_with_double(self, rows_with_double):
        # get the columns in the possibilities matrix with only two potential values
        cols_with_double = self.table_idx[rows_with_double, 1]
        return cols_with_double

    def get_zones_with_double(self, rows_with_double):
        # get the zone index of cells with only two potential values
        zones_with_double = self.zone_idx[rows_with_double, :]
        return zones_with_double

    def get_total_possibilities(self):
        # get the total number of possibilities in remaining unmarked cells
        total_possibilities = self.possibilities.nonzero()[0].shape[0]
        return total_possibilities

    def set_single_possibility(self, rows, val):
        # set a single possibility to a specific row in the possibilities matrix
        if rows.size == 1:
            self.possibilities[rows, :] = np.zeros(self.possibilities.shape[1])
        else:
            self.possibilities[rows, :] = np.zeros([rows.shape[0], self.possibilities.shape[1]])

        self.possibilities[rows, 0] = val

    def slice_class(self, rows_to_keep):
        # keep specific unmarked cells of the table_idx, zone_idz, and possibilities matrix
        if rows_to_keep.shape[0] == 0:
            self.table_idx = np.array([])
            self.zone_idx = np.array([])
            self.possibilities = np.array([])
        else:
            self.table_idx = self.table_idx[rows_to_keep, :]
            self.zone_idx = self.zone_idx[rows_to_keep, :]
            self.possibilities = self.possibilities[rows_to_keep, :]

        self.num = rows_to_keep.shape[0]

    def clean_value_in_scope(self, val, idx, scope):
        # removes a value in all unmarked cells in a specified zone, column, or row
        for v, i in zip(val, idx):

            # find rows matching scope with only 1 possibility zone
            if scope == "zone":
                scope_match_rows = np.all(self.zone_idx == i, axis=1).nonzero()[0]
            elif scope == "row":
                scope_match_rows = self.table_idx[:, 0] == i
            elif scope == "col":
                scope_match_rows = self.table_idx[:, 1] == i
            else:
                print "Invalid scope"
                return

            # get possible values in unmarked cells in the same zone
            val = self.possibilities[scope_match_rows, :]

            # set possible values that match the current value to 0
            val[val == v] = 0

            # push results back into possibilities
            self.possibilities[scope_match_rows, :] = val

    def clean_pairs_in_scope(self, scope):
        # remove a pair of values in all unmarked cells in a specified zone, column, or row

        rows_with_double = self.get_rows_with_n_possibilities(2)
        doubles_possibilities = self.get_double_possibilities(rows_with_double)

        # extract zone, row, or columns with only two possibilities
        if scope == "zone":
            double_idx = self.get_zones_with_double(rows_with_double)
        elif scope == "row":
            double_idx = self.get_table_rows_with_double(rows_with_double)
        elif scope == "col":
            double_idx = self.get_table_cols_with_double(rows_with_double)
        else:
            print "Invalid scope"
            return

        # loop through to find matching values within the same scope
        for doubles, idx in zip(doubles_possibilities, double_idx):

            # find unmarked with matching values
            match_doubles = np.all(doubles_possibilities == doubles, axis=1)

            if scope == "zone":
                match_scope = np.all(double_idx == idx, axis=1)
            elif scope in {"row", "col"}:
                match_scope = double_idx == idx
            else:
                print "Invalid scope"
                return

            # find unmarked with matching values in the same zones
            pair_matched = np.all(np.concatenate([[match_scope], [match_doubles]]), axis=0)

            # if a match is found, clean scope
            if sum(pair_matched) == 2:
                if scope == "zone":
                    index = np.array([idx])
                elif scope in {"row", "col"}:
                    index = np.array([idx, idx])
                else:
                    print "Invalid scope"
                    return

                self.clean_value_in_scope(doubles, index, scope)

                # refill possibilities for pairs due to deletion in cleaning
                curr_double = np.concatenate([doubles, np.zeros(self.ZONE_SIZE**2-2)])
                self.possibilities[rows_with_double[pair_matched], :] = curr_double

    def clean_singles_in_scope(self, scope):
        # look for a single occurrence of a possibility within a specified zone, row or column

        # loop through each column and look for single potential values
        for idx in range(self.ZONE_SIZE**2):

            # find unmarked rows with matching table rows
            if scope == "zone":
                zone_x = idx % self.ZONE_SIZE
                zone_y = np.floor(idx/self.ZONE_SIZE)
                match_scope_rows = np.all(self.zone_idx == [zone_x, zone_y], axis=1)
            elif scope == "row" or scope == "col":
                match_scope_rows = self.table_idx[:, 0] == idx

            # get possibilities with matching table rows
            rows_matching_scope_possibilities = self.possibilities[match_scope_rows, :]
            match_scope_possibilities = rows_matching_scope_possibilities[rows_matching_scope_possibilities.nonzero()]

            # count number of occurrences for each possibility
            possibilities_cnt = np.bincount(match_scope_possibilities.astype(int))
            single_val_in_scope = np.where(possibilities_cnt == 1)[0]

            # modify the possibilities matrix for a single occurrence of a possibility within a scope
            if single_val_in_scope.shape[0] > 0:

                if single_val_in_scope.shape[0] == 1:
                    match_row, match_col = np.where(rows_matching_scope_possibilities == single_val_in_scope)
                    rows_matching_scope_possibilities[match_row, :] = np.zeros(self.ZONE_SIZE**2)
                    rows_matching_scope_possibilities[match_row, 0] = single_val_in_scope
                    self.possibilities[match_scope_rows, :] = rows_matching_scope_possibilities
                else:
                    for val in single_val_in_scope:
                        match_row, match_col = np.where(rows_matching_scope_possibilities == val)

                        rows_matching_scope_possibilities[match_row, :] = np.zeros(self.ZONE_SIZE**2)
                        rows_matching_scope_possibilities[match_row, 0] = val
                        self.possibilities[match_scope_rows, :] = rows_matching_scope_possibilities

    def solved(self):
        # determine if there are no more unmarked cells signifying a solved sudoku
        sudoku_solved = self.num == 0
        return sudoku_solved
