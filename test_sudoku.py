__author__ = 'aouyang1'

import unittest
import sudoku_main
import os
import numpy as np


class MyTestCase(unittest.TestCase):

    num_examples = 50

    def test_level1(self):
        num_errors = np.ones(self.num_examples)
        for num in range(1, self.num_examples+1):
            fname = 'level1/sudoku_level1_' + str(num) + '.csv'
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
            num_errors[num-1] = curr_errors
        self.assertEqual(any(num_errors), False)

    def test_level2(self):
        num_errors = np.ones(self.num_examples)
        for num in range(1, self.num_examples+1):
            fname = 'level2/sudoku_level2_' + str(num) + '.csv'
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
            num_errors[num-1] = curr_errors
        self.assertEqual(any(num_errors), False)

    def test_level3(self):
        num_errors = np.ones(self.num_examples)
        for num in range(1, self.num_examples+1):
            fname = 'level3/sudoku_level3_' + str(num) + '.csv'
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
            num_errors[num-1] = curr_errors
        self.assertEqual(any(num_errors), False)

    def test_level4(self):
        num_errors = np.ones(self.num_examples)
        for num in range(1, self.num_examples+1):
            fname = 'level4/sudoku_level4_' + str(num) + '.csv'
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
            num_errors[num-1] = curr_errors
        self.assertEqual(any(num_errors), False)

if __name__ == '__main__':
    unittest.main()
