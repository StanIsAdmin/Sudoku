"""
A library designed to create, display (command line) and solve sudoku puzzles
"""

allowedValues = frozenset([1,2,3,4,5,6,7,8,9])
blankValue = 0

class SetOfNine:

	def __init__(self, values):
		#todo: check if size is correct
		self.values = values


	def isValid(self, allowBlanks=True):
		found = [False for i in range(9)] #bool : has the value been found
	
		#for each value of the group
		for value in self.values:
			#if it's a blank
			if (value == blankValue):
				if not allowBlanks:
					return False

			#if it's another value
			else:
				if (found[value-1]):
					return False
				else:
					found[value-1] = True
		return True

	def isComplete(self):
		return self.isValid(False)
		


class Sudoku:
	
	#static variables
	allowedValues = [1,2,3,4,5,6,7,8,9]
	blankValue = 0

	def __init__(self, valuesMatrix=[]):
		#todo: check if size and type are correct
		self.values = valuesMatrix
		

	def createFromInput(self):
		"""
		Create the sudoku by asking for input via the command line
		"""
		self.values = []
		while len(self.values) < 9:
			#ask for values, blanks can be spaces or zeroes
			userInput = input("Line " + str(len(self.values) + 1) + " : ").replace(" ", "0")
		
			#complete the end of the line with blanks if line is too short		
			if len(userInput) < 9:
				userInput += "0"*(9-len(userInput))
		
			#check number and type of values	 
			if len(userInput) == 9 and userInput.isdigit():
				self.values.append(list(map(int, userInput))) #add line to values matrix
			else:
				print("Invalid input")
	
		#check if the values are valid for a sudoku
		if not self.isValid():
			self.values = []
			print("Not a valid sudoku, values discarded")

	def getLine(self, index):
		return SetOfNine(self.values[index][:])

	def getColumn(self, index):
		return SetOfNine([self.values[i][index] for i in range(9)])

	def getBox(self, index):
		topLine = (index//3)%3 *3
		leftColumn = index%3 *3
		return SetOfNine([self.values[line][column] for line in range(topLine, topLine+3) \
										for column in range(leftColumn, leftColumn+3)])

	def getLines(self):
		for i in range(9):
			yield self.getLine(i)

	def getColumns(self):
		for i in range(9):
			yield self.getColumn(i)

	def getBoxes(self):
		for i in range(9):
			yield self.getBox(i)

	def getGroups(self):
		for line in self.getLines():
			yield line
		for column in self.getColumns():
			yield column
		for square in self.getBoxes():
			yield square

	def isValid(self):	
		for group in self.getGroups():
			if not group.isValid():
				return False
		return True

	def isComplete(self):
		for group in self.getGroups():
			if not group.isComplete():
				return False
		return True

	def __repr__(self):
		lineList = []
		for line in range(9):
			#separator for groups of 3 lines
			if line%3==0 and line!=0: 
				lineList.append("_________|_________|_________")
				lineList.append("         |         |         ")

		
			#blank line
			lineChars = list(" _  _  _ | _  _  _ | _  _  _")

			#fill the blanks		
			for column in range(9):
					offset = 1 + (column*3) + (column//3)
					value = self.values[line][column]
					if value != blankValue:
						lineChars[offset] = str(value)
			lineList.append(''.join(lineChars))
		return "\n".join(lineList)
