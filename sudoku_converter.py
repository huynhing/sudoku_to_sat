#String variables
BOOLEAN = " : BOOLEAN;"
NEW_LINE = "\n"
X_VAR = "x"
Y_VAR = "y"
UNDERSCORE = "_"
ASSERT = "ASSERT("
END_ASSERT = ");"
AND = " AND "
OR = " OR "
NOT = "NOT"
BEGIN_PAR = "("
END_PAR = ")"
IMP = "=>"
SPACE = " "

def sudoku_converter(sudoku_csv):
	stp_program = open("sudoku_stp.in", "w")

	#CREATE BOOLEAN VARIABLES
	for y in range(9):
		for x in range(9):
			nine_var = []
			for value in range(9):
				nine_var.append(X_VAR + str(x+1) + Y_VAR + str(y+1) + UNDERSCORE + str(value+1))
			stp_program.write(", ".join(nine_var) + BOOLEAN + NEW_LINE) #WRITE TO PROGRAM!

	sudoku_board = open(sudoku_csv, "r")
	#ASSERT WHICH ENTRIES ARE TRUE NUM_XCOORD_YCOORD
	y_counter = 1 #KEEP TRACK OF Y COORDINATE
	for line in sudoku_board.read().splitlines():
		x_counter = 1 #KEEP TRACK OF X COORDINATE
		for entry in line.split(","):
			if entry != SPACE: #ENTRY IN BOX
				variable_assignment = X_VAR + str(x_counter) + Y_VAR + str(y_counter) + UNDERSCORE + entry
				stp_program.write(ASSERT + variable_assignment + END_ASSERT + NEW_LINE) #WRITE TO PROGRAM
			x_counter += 1
		y_counter += 1
	sudoku_board.close()

	#BASIC SOLVING CONSTRAINTS:
	#ROWS
	for y in range(9):
		nine_var_and = []
		for x in range(9):
			nine_var_or = []
			for value in range(9):
				nine_var_or.append(X_VAR + str(x+1) + Y_VAR + str(y+1) + UNDERSCORE + str(value+1))
			nine_var_and.append(BEGIN_PAR + OR.join(nine_var_or) + END_PAR)
		stp_program.write(ASSERT + AND.join(nine_var_and) + END_ASSERT + NEW_LINE)
	#COLUMNS
	for x in range(9):
		nine_var_and = []
		for y in range(9):
			nine_var_or = []
			for value in range(9):
				nine_var_or.append(X_VAR + str(x+1) + Y_VAR + str(y+1) + UNDERSCORE + str(value+1))
			nine_var_and.append(BEGIN_PAR + OR.join(nine_var_or) + END_PAR)
		stp_program.write(ASSERT + AND.join(nine_var_and) + END_ASSERT + NEW_LINE)

	#VALUE CONSTRAINTS
	for x in range(9):
		for y in range(9):
			for value in range(9):
				#ROW VALUE CONSTRAINTS
				row_imp = []
				left_imp = X_VAR + str(x+1) + Y_VAR + str(y+1) + UNDERSCORE + str(value+1)
				for not_x in range(9):
					if not_x != x:
						right_imp = X_VAR + str(not_x+1) + Y_VAR + str(y+1) + UNDERSCORE + str(value+1)
						row_imp.append(NOT + BEGIN_PAR + right_imp + END_PAR)
				row_implication = left_imp + SPACE + IMP + SPACE + BEGIN_PAR + AND.join(row_imp) + END_PAR
				stp_program.write(ASSERT + row_implication + END_ASSERT + NEW_LINE)
				#COLUMN VALUE CONSTRAINTS
				col_imp = []
				for not_y in range(9):
					if not_y != y:
						right_imp = X_VAR + str(x+1) + Y_VAR + str(not_y+1) + UNDERSCORE + str(value+1)
						col_imp.append(NOT + BEGIN_PAR + right_imp + END_PAR)
				col_implication = left_imp + SPACE + IMP + SPACE + BEGIN_PAR + AND.join(col_imp) + END_PAR
				stp_program.write(ASSERT + col_implication + END_ASSERT + NEW_LINE)

	#3x3 BLOCK CONSTRAINTS
	for x in range(9):
		for y in range(9):
			for value in range(9):
				block_imp = []
				left_imp = X_VAR + str(x+1) + Y_VAR + str(y+1) + UNDERSCORE + str(value+1)
				left_bound, right_bound, top_bound, bottom_bound = establish_block_bounds(x+1, y+1)
				not_x = left_bound
				while not_x <= right_bound:
					not_y = top_bound
					while not_y <= bottom_bound:
						if not_x != x+1 or not_y != y+1:
							right_imp = X_VAR + str(not_x) + Y_VAR + str(not_y) + UNDERSCORE + str(value+1)
							block_imp.append(NOT + BEGIN_PAR + right_imp + END_PAR)
						not_y += 1
					not_x += 1
				block_implication = left_imp + SPACE + IMP + SPACE + BEGIN_PAR + AND.join(block_imp) + END_PAR
				stp_program.write(ASSERT + block_implication + END_ASSERT + NEW_LINE)

	stp_program.close()

def establish_block_bounds(x, y):
	right_bound = left_bound = None
	top_bound = bottom_bound = None
	if x % 3 == 0: #RIGHT
		right_bound = x
		left_bound = x - 2
	elif x % 3 == 2: #MIDDDLE
		right_bound = x + 1
		left_bound = x - 1
	else: #LEFT
		right_bound = x + 2
		left_bound = x

	if y % 3 == 0: #BOTTOM
		top_bound = y - 2
		bottom_bound = y
	elif y % 3 == 2: #MIDDLE
		top_bound = y - 1
		bottom_bound = y + 1
	else: #TOP
		top_bound = y
		bottom_bound = y + 2
	return left_bound, right_bound, top_bound, bottom_bound

import sys
sudoku_converter(sys.argv[1])