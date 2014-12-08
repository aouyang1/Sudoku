__author__ = 'aouyang1'
import sudoku_main
import os
import numpy as np

if __name__ == "__main__":

    """
    ------------------------------------------
    Define testing parameters
    - level selection = 1, 2, 3, 4
    - max tests = 50
    ------------------------------------------
    """
    level_select = [1, 2, 3, 4]
    num_tests = 10

    num_errors = np.ones([4, num_tests])

    for level in level_select:
        for num in range(1, num_tests+1):
            fname = '../level' + str(level) + '/sudoku_level' + str(level) + '_' + str(num) + '.csv'
            sudoku_main.main(fname)

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
    print "-----------------------"
    for level in level_select:
        print "level {}: {} % out of {} ".format(level, percent_correct[level-1], num_tests)


