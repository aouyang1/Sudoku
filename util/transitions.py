"""
Transition class containing the functions for the next state in the finite state machine:

- 'initialize_transitions', initialize Sudoku table and brute force class
- 'single_unmarked_transitions', detect unmarked cells with only one possibility
- 'matching_pairs_in_zone_transitions', identify matching pairs within the same zone
- 'matching_pairs_in_row_transitions', identify matching pairs within the same row
- 'matching_pairs_in_col_transitions', identity matching pairs within the same col
- 'single_in_zone_transitions', identify single occurrence of a possibility within a zone
- 'single_in_row_transitions', identify single occurrence of a possibility within a row
- 'single_in_col_transitions', identify single occurrence of a possibility within a column
- 'stuck_transitions', setting up or continuing a brute force approach when all other strategies have been exhausted
- 'error_transitions', determine whether to continue brute force approach or show current results after an error
- 'show_results', display the solved table and the output csv file
- 'create_table', initialize Sudoku class after reading table from csv file
"""

import os

import numpy as np
from util.sudokutable import SudokuTable
from util.bruteforce import BruteForce


class Transitions:

    def initialize_transitions(self, sudoku_table_fname):
        # transition function initializing the sudoku table and brute force class
        Sudoku = self.create_table(sudoku_table_fname)
        Sudoku.initialize_unmarked()
        Brute = BruteForce()

        new_state = "single_unmarked_state"

        return new_state, (Sudoku, Brute)

    @staticmethod
    def single_unmarked_transitions((Sudoku, Brute)):
        # transition function detecting unmarked cells with only one possibility

        rows_with_only_one = Sudoku.unmarked.get_rows_with_n_possibilities(1)
        single_unmarked_found = rows_with_only_one.shape[0] != 0

        if single_unmarked_found:
            Sudoku.fill_and_update_table(rows_with_only_one)
            rows_to_keep = np.array(list(set(rows_with_only_one) ^ set(np.arange(Sudoku.unmarked.num))))
            Sudoku.unmarked.slice_class(rows_to_keep)
            Sudoku.check_for_error()

        if Sudoku.error_status:
            new_state = "error_state"
        elif Sudoku.unmarked.solved():
            new_state = "show_results_state"
        elif single_unmarked_found:
            new_state = "single_unmarked_state"
        else:
            new_state = "matching_pairs_in_zone_state"

        return new_state, (Sudoku, Brute)

    @staticmethod
    def matching_pairs_in_zone_transitions((Sudoku, Brute)):
        # transition function identifying matching pairs within the same zone

        old_num_possibilities = Sudoku.unmarked.get_total_possibilities()

        Sudoku.unmarked.clean_pairs_in_scope(scope="zone")

        new_num_possibilities = Sudoku.unmarked.get_total_possibilities()
        possibilities_changed = old_num_possibilities != new_num_possibilities

        if Sudoku.unmarked.solved():
            new_state = "show_results_state"
        elif possibilities_changed:
            new_state = "single_unmarked_state"
        else:
            new_state = "matching_pairs_in_row_state"

        return new_state, (Sudoku, Brute)

    @staticmethod
    def matching_pairs_in_row_transitions((Sudoku, Brute)):
        # transition function identifying matching pairs within the same row

        old_num_possibilities = Sudoku.unmarked.get_total_possibilities()

        Sudoku.unmarked.clean_pairs_in_scope(scope="row")

        new_num_possibilities = Sudoku.unmarked.get_total_possibilities()
        possibilities_changed = old_num_possibilities != new_num_possibilities

        if Sudoku.unmarked.solved():
            new_state = "show_results_state"
        elif possibilities_changed:
            new_state = "single_unmarked_state"
        else:
            new_state = "matching_pairs_in_col_state"

        return new_state, (Sudoku, Brute)

    @staticmethod
    def matching_pairs_in_col_transitions((Sudoku, Brute)):
        # transition function identifying matching pairs within the same column

        old_num_possibilities = Sudoku.unmarked.get_total_possibilities()

        Sudoku.unmarked.clean_pairs_in_scope(scope="col")

        new_num_possibilities = Sudoku.unmarked.get_total_possibilities()
        possibilities_changed = old_num_possibilities != new_num_possibilities

        if Sudoku.unmarked.solved():
            new_state = "show_results_state"
        elif possibilities_changed:
            new_state = "single_unmarked_state"
        else:
            new_state = "single_in_zone_state"

        return new_state, (Sudoku, Brute)

    @staticmethod
    def single_in_zone_transitions((Sudoku, Brute)):
        # transition function identifying a single occurrence of a possibility within a zone

        old_num_possibilities = Sudoku.unmarked.get_total_possibilities()

        Sudoku.unmarked.clean_singles_in_scope(scope="zone")

        new_num_possibilities = Sudoku.unmarked.get_total_possibilities()
        possibilities_changed = old_num_possibilities != new_num_possibilities

        # next state logic
        if Sudoku.unmarked.solved():
            new_state = "show_results_state"
        elif possibilities_changed:
            new_state = "single_unmarked_state"
        else:
            new_state = "single_in_row_state"

        return new_state, (Sudoku, Brute)

    @staticmethod
    def single_in_row_transitions((Sudoku, Brute)):
        # transition function identifying a single occurrence of a possibility within a row

        old_num_possibilities = Sudoku.unmarked.get_total_possibilities()

        Sudoku.unmarked.clean_singles_in_scope(scope="row")

        new_num_possibilities = Sudoku.unmarked.get_total_possibilities()
        possibilities_changed = old_num_possibilities != new_num_possibilities

        # next state logic
        if Sudoku.unmarked.solved():
            new_state = "show_results_state"
        elif possibilities_changed:
            new_state = "single_unmarked_state"
        else:
            new_state = "single_in_col_state"

        return new_state, (Sudoku, Brute)

    @staticmethod
    def single_in_col_transitions((Sudoku, Brute)):
        # transition function identifying a single occurrence of a possibility within a column

        old_num_possibilities = Sudoku.unmarked.get_total_possibilities()

        Sudoku.unmarked.clean_singles_in_scope(scope="col")

        new_num_possibilities = Sudoku.unmarked.get_total_possibilities()
        possibilities_changed = old_num_possibilities != new_num_possibilities

        # next state logic
        if Sudoku.unmarked.solved():
            new_state = "show_results_state"
        elif possibilities_changed:
            new_state = "single_unmarked_state"
        else:
            new_state = "stuck_state"

        return new_state, (Sudoku, Brute)

    @staticmethod
    def stuck_transitions((Sudoku, Brute)):
        # transition function setting up or continuing a brute force approach when all
        # other strategies have been exhausted

        if not Brute.status:
            Brute.status = True
            Brute.sudoku.copy_sudoku(Sudoku)
            Sudoku.setup_brute_force()

            new_state = 'single_unmarked_state'
        else:
            row, col = Brute.sudoku.unmarked.get_possibilities_index()
            brute_force_finished = Brute.possibilities_cnt == row.shape[0]-1

            if brute_force_finished:
                new_state = 'show_results_state'
            else:
                Sudoku.copy_sudoku(Brute.sudoku)

                Brute.possibilities_cnt += 1
                val = Sudoku.unmarked.possibilities[row[Brute.possibilities_cnt],
                                                    col[Brute.possibilities_cnt]]

                Sudoku.unmarked.set_single_possibility(row[Brute.possibilities_cnt], val)

                new_state = 'single_unmarked_state'

        return new_state, (Sudoku, Brute)

    @staticmethod
    def error_transitions((Sudoku, Brute)):
        # transition function determining whether to continue brute force approach or
        # show current results after an error

        Sudoku.error_status = False

        # if error occurred, log error and try again with new starting value
        if Brute.status:
            new_state = "stuck_state"
        else:
            new_state = "show_results_state"

        return new_state, (Sudoku, Brute)

    @staticmethod
    def show_results_transitions((Sudoku, Brute)):
        # transition function displaying the solved table and the name of the output csv file

        new_state = "finished_state"

        # write solved table to csv file
        dir_name = os.path.dirname(Sudoku.fname)
        input_name = os.path.basename(Sudoku.fname)
        split_input_name = os.path.splitext(input_name)
        solved_name = os.path.join(dir_name, split_input_name[0] + "_solved" + split_input_name[1])
        np.savetxt(solved_name, Sudoku.table.astype(int), fmt='%d', delimiter=',')

        return new_state, (Sudoku, Brute)

    @staticmethod
    def create_table(sudoku_table_fname):
        # initializes the sudoku table after reading the table from a file

        # read sudoku csv file
        sudoku_table = np.genfromtxt(sudoku_table_fname, delimiter=",")

        print "solving {}".format(sudoku_table_fname)

        # find rows, columns in table that need to be solved
        table_row, table_col = np.where(sudoku_table == 0)

        # initialize table_idx, zone_idx, possibilities
        num_unmarked = len(table_row)
        unmarked_table_idx = np.concatenate([table_row.reshape(num_unmarked, 1),
                                             table_col.reshape(num_unmarked, 1)], axis=1)

        # instantiate SudokuTable class
        Sudoku = SudokuTable(fname=sudoku_table_fname,
                             table=sudoku_table,
                             unmarked_table_idx=unmarked_table_idx)

        return Sudoku

