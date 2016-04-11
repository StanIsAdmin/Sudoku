"""
A library designed to create, display (command line) and solve sudoku puzzles
"""
allowedValues = [1,2,3,4,5,6,7,8,9]
blankValue = 0

def askValues():
	"""
	Asks for input via the command line
	"""
	sudokuValues = [] #sudoku matrix
	while len(sudokuValues) < 9:
		
		#ask for values, blanks can be spaces or zeroes
		userInput = input("Line " + str(len(sudokuValues) + 1) + " : ").replace(" ", "0")
		
		#complete the end of the line with blanks if line is too short		
		if len(userInput) < 9:
			userInput += "0"*(9-len(userInput))
		
		#check number and type of values	 
		if len(userInput) == 9 and userInput.isdigit():
			sudokuValues.append(list(map(int, userInput))) #add line to matrix
		else:
			print("Invalid input")
	
	#check if the values are valid for a sudoku
	if not isValid(sudokuValues):
		sudokuValues = []
	
	return sudokuValues

def getLine(sudokuValues, index):
	return sudokuValues[index][:]

def getLines(sudokuValues):
	for i in range(9):
		yield getLine(sudokuValues, i)

def getColumn(sudokuValues, index):
	return [sudokuValues[i][index] for i in range(9)]

def getColumns(sudokuValues):
	for i in range(9):
		yield getColumn(sudokuValues, i)

def getSquare(sudokuValues, index):
	topLine = (index//3)%3 *3
	leftColumn = index%3 *3
	return [sudokuValues[line][column] for line in range(topLine, topLine+3) \
									for column in range(leftColumn, leftColumn+3)]

def getSquares(sudokuValues):
	for i in range(9):
		yield getSquare(sudokuValues, i)

def groupHasDuplicates(groupValues):
	groupValues.sort()
	for i in range(8):
		if groupValues[i] != blankValue and groupValues[i]==groupValues[i+1]:
			return True
	return False

def getGroups(sudokuValues):
	for line in getLines(sudokuValues):
		yield line
	for column in getColumns(sudokuValues):
		yield column
	for square in getSquares(sudokuValues):
		yield square

def isValid(sudokuValues):	
	#Check if horizontal lines don't have duplicates
	for group in getGroups(sudokuValues):
		if groupHasDuplicates(group):
			return False
	return True
				

def show(sudokuValues):
	for line in range(9):
		#separator for groups of 3 lines
		if line%3==0 and line!=0: 
			print("_________|_________|_________")
			print("         |         |         ")

		
		#blank line
		lineChars = list(" _  _  _ | _  _  _ | _  _  _")

		#fill the blanks		
		for column in range(9):
				offset = 1 + (column*3) + (column//3)
				value = sudokuValues[line][column]
				if value != blankValue:
					lineChars[offset] = str(value)
		print(''.join(lineChars))
