Sudoku
======

## What

Solves a [Sudoku](http://www.sudoku.name/rules/en) puzzle in a csv file format where zeros represent unsolved cells and writes the solution to the same input directory. filename_solved.csv

Input example:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Output example:<br/>
_foo.csv_&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_foo_solved.csv_<br/>
_**0**_,&nbsp;3,&nbsp;5,&nbsp;2,&nbsp;9,&nbsp;_**0**_,&nbsp;8,&nbsp;6,&nbsp;4&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1,&nbsp;3,&nbsp;5,&nbsp;2,&nbsp;9,&nbsp;7,&nbsp;8,&nbsp;6,&nbsp;4<br/>
_**0**_,&nbsp;8,&nbsp;2,&nbsp;4,&nbsp;1,&nbsp;_**0**_,&nbsp;7,&nbsp;_**0**_,&nbsp;3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;9,&nbsp;8,&nbsp;2,&nbsp;4,&nbsp;1,&nbsp;6,&nbsp;7,&nbsp;5,&nbsp;3<br/>
7,&nbsp;6,&nbsp;4,&nbsp;3,&nbsp;8,&nbsp;_**0**_,&nbsp;_**0**_,&nbsp;9,&nbsp;_**0**_&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;7,&nbsp;6,&nbsp;4,&nbsp;3,&nbsp;8,&nbsp;5,&nbsp;1,&nbsp;9,&nbsp;2<br/>
2,&nbsp;1,&nbsp;8,&nbsp;7,&nbsp;3,&nbsp;9,&nbsp;_**0**_,&nbsp;4,&nbsp;_**0**_&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2,&nbsp;1,&nbsp;8,&nbsp;7,&nbsp;3,&nbsp;9,&nbsp;6,&nbsp;4,&nbsp;5<br/>
_**0**_,&nbsp;_**0**_,&nbsp;_**0**_,&nbsp;8,&nbsp;_**0**_,&nbsp;4,&nbsp;2,&nbsp;3,&nbsp;_**0**_&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;5,&nbsp;9,&nbsp;7,&nbsp;8,&nbsp;6,&nbsp;4,&nbsp;2,&nbsp;3,&nbsp;1<br/>
_**0**_,&nbsp;4,&nbsp;3,&nbsp;_**0**_,&nbsp;5,&nbsp;2,&nbsp;9,&nbsp;7,&nbsp;_**0**_&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;6,&nbsp;4,&nbsp;3,&nbsp;1,&nbsp;5,&nbsp;2,&nbsp;9,&nbsp;7,&nbsp;8<br/>
4,&nbsp;_**0**_,&nbsp;6,&nbsp;5,&nbsp;7,&nbsp;1,&nbsp;_**0**_,&nbsp;_**0**_,&nbsp;9&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4,&nbsp;2,&nbsp;6,&nbsp;5,&nbsp;7,&nbsp;1,&nbsp;3,&nbsp;8,&nbsp;9<br/>
3,&nbsp;5,&nbsp;9,&nbsp;_**0**_,&nbsp;2,&nbsp;8,&nbsp;4,&nbsp;1,&nbsp;7&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3,&nbsp;5,&nbsp;9,&nbsp;6,&nbsp;2,&nbsp;8,&nbsp;4,&nbsp;1,&nbsp;7<br/>
8,&nbsp;_**0**_,&nbsp;_**0**_,&nbsp;9,&nbsp;_**0**_,&nbsp;_**0**_,&nbsp;5,&nbsp;2,&nbsp;6&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;8,&nbsp;7,&nbsp;1,&nbsp;9,&nbsp;4,&nbsp;3,&nbsp;5,&nbsp;2,&nbsp;6<br/>

## Approach
First link potential number possibilities with each unsolved cell<br/>
Uses a state machine with various puzzle strategies to reduce possibilities in each unsoved cell.<br/>
Strategies:
- s1: matching possibility pairs in the same zone: all possibilities in the same zone with the same pair are deleted
- s3: matching possibility pairs in the same row: all possibilities in the same row with the same pair are deleted
- s4: matching possibility pairs in the same column: all possibilities in the same column with the same pair are deleted
- s5: single occurence of a possibility in a zone: replace unsolved cell with possibility
- s6: single occurence of a possibility in a row: replace unsolved cell with possibility
- s7: single occurence of a possibility in a column: replace unsolved cell with possibility
- s8: brute force search: trial and error test of remaining possibilities for each cell until finish condition met

![GitHub Logo](/images/Sudoku_statemachine_cropped.png)

## How
### Running
Terminal example:  
$ python sudoku_main.py  
Enter path of csv file: level1/sudoku_level1_1.csv  

### Testing
50 Sudoku puzzles have been extracted from QQwing website with levels 1-4 (easy-hard)  
Testing data can be found in the level1, level2, level3, and level4 folders  
Each test represents a specific difficulty with 50 test problems. The test solves each problem and compares directly with the expected solution.

Terminal example:  
$ nosetests -v --with-timer

