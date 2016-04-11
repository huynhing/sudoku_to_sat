# sudoku_to_sat
A sudoku to SAT problem converter for CS170.
The solver takes in a CSV of the sudoku board (with spaces where empty entries are) and converts it to SAT problem.
An example board is given along with its raw solution (both false and true variables) and complete solution (just true variables).
Code can be more efficient by combining some loops, but it is done in a way where the output problem looks nice/organized.

INPUT
-----
CSV of sudoku board with spaces where empty entries are.

OUTPUT
------
SAT problem for a STP solver.
