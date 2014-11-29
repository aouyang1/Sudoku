__author__ = 'Austin Ouyang'

import os
from statemachine import StateMachine
from transitions import Transitions
import numpy as np


if __name__ == "__main__":
    m = StateMachine()
    t = Transitions()       # next state functions for state machine

    m.add_state("initialize_state", t.initialize_transitions)
    m.add_state("single_unmarked_state", t.single_unmarked_transitions)
    m.add_state("matching_pairs_in_zone_state", t.matching_pairs_in_zone_transitions)
    m.add_state("matching_pairs_in_row_state", t.matching_pairs_in_row_transitions)
    m.add_state("matching_pairs_in_col_state", t.matching_pairs_in_col_transitions)
    m.add_state("single_in_zone_state", t.single_in_zone_transitions)
    m.add_state("single_in_row_state", t.single_in_row_transitions)
    m.add_state("single_in_col_state", t.single_in_col_transitions)
    m.add_state("show_results_state", t.show_results_transitions)
    m.add_state("stuck_state", t.stuck_transitions)
    m.add_state("error_state", t.error_transitions)

    m.add_state("finished_state", None, end_state=1)

    m.set_start("initialize_state")

    num_errors = np.ones([4, 50])
    num_tests = 50
    num_levels = 4
    for level in range(1, num_levels+1):
        for num in range(1, num_tests+1):
            fname = 'level' + str(level) + '\\sudoku_level' + str(level) + '_' + str(num) + '.csv'
            m.run(fname)

            dir_name = os.path.dirname(fname)
            input_name = os.path.basename(fname)
            split_input_name = os.path.splitext(input_name)

            # read in solution csv file
            solution_name = os.path.join(dir_name, split_input_name[0] + "_solution" + split_input_name[1])
            solution = np.genfromtxt(solution_name, delimiter=",")

            # read in solved csv file
            solved_name = os.path.join(dir_name, split_input_name[0] + "_solved" + split_input_name[1])
            solved = np.genfromtxt(solution_name, delimiter=",")

            curr_errors = sum(sum((solution - solved) != 0))
            num_errors[level-1, num-1] = curr_errors

    percent_correct = np.sum(num_errors == 0, axis=1)/num_tests*100

    print "-----------------------------------------"
    for level in range(0, num_levels):
        print "level {} {} percent correct: ".format(level+1, percent_correct[level])


