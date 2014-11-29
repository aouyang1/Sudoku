"""
converts QQwing csv format to format specified by the Insight data engineering coding challenge
"""

import numpy as np

level = 1   # level associated with sudoku tables in QQWING.csv file

a = np.genfromtxt('QQWING.csv', dtype=str, delimiter=',')
a = a[:, :2]
print a

for n in range(a.shape[0]):

    problem = a[n][0].replace('.', '0')
    solution = a[n][1]

    problem = np.array([int(problem[i]) for i in range(81)]).reshape(9, 9)
    solution = np.array([int(solution[i]) for i in range(81)]).reshape(9, 9)

    np.savetxt("level" + str(level) + "\sudoku_level" + str(level) + "_" + str(n+1) + '.csv', problem, fmt='%d', delimiter=',')
    np.savetxt("level" + str(level) + "\sudoku_level" + str(level) + "_" + str(n+1) + '_solution.csv', solution, fmt='%d', delimiter=',')