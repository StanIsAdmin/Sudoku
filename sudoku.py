"""
A library designed to create, display (command line) and solve sudoku puzzles.
"""

#Allowed sizes for the sudoku's boxes
minBoxSize=2
maxBoxSize=8

#Allowed sizes for the sudoku's table
minTableSize=minBoxSize**2
maxTableSize=maxBoxSize**2



class PreemptiveSet:
	"""
	A preemptive set is a list of m values, each of them between 1 and m, together with a list of m cells, with the property that no values other than the m values from the list can occupy the m cells. Values that do not occupy a cell yet are called free.
	"""

	def __init__(self, boxSize, cellList):
		"""
		Creates an instance of PreemptiveSet with the list of cells cellList and a full set of free values.
		Raises ValueError if boxSize is not in the range (minBoxSize, maxBoxSize) or if cellList is not a list of tableSize Cells.
		Raises Exception if all cells from cellList are not blank.
		"""
		#check type and range of boxSize
		if not (isinstance(boxSize, int) and boxSize>=minBoxSize and boxSize<=maxBoxSize):
			raise ValueError
		#check type and size of cellList
		if not (isinstance(cellList, list) and len(cellList)==boxSize**2):
			raise ValueError
		#check type of cellList's elements
		for cell in cellList:
			if not (isinstance(cell, Cell)):
				raise ValueError
		#check if all cells are blank
		for cell in cellList:
			if not cell.isBlank():
				raise Exception("Cell in preemptive set not blank")
		
		self._cells = cellList #preemptive set's cells
		self._freeValues = set([i for i in range(1, boxSize**2 +1)])

	def getCells(self):
		"""
		Generator returning the preemptive set's cells.
		"""
		for cell in self._cells:
			yield cell
	
	def valueIsFree(self, value):
		"""
		Returns True if one of the Cells has value as its value, False otherwise.
		Raises ValueError if value is not in the range (1, tableSize)
		"""
		#check value type and range
		if not (isinstance(value, int) and value>=1 and value <=len(self._cells)):
			raise ValueError
		
		#True if value belongs to freeValues
		return value in self._freeValues

	def getFreeValues(self):
		"""
		Returns a set containing the free values of the preemptive set.
		"""
		return self._freeValues.copy()
	
	def isComplete(self):
		"""
		Returns True if each cell of the preemptive set's values is in exactly one cell, False otherwise.
		"""
		#empty set of free values will be converted to False, non empty set to True
		return not bool(self._freeValues)



class Cell:
	"""
	Class representing a cell of the sudoku table.
	A Cell is either blank or has a value, that can range from 1 to the sudoku's tableSize.
	A Cell has markup values, which are the values it can hold without violating the sudoku rules.
	"""

	def __init__(self, boxSize):
		"""
		Creates an instance of Cell allowing values in the range (1, boxSize**2).
		Upon construction, the Cell is Blank.
		Raises ValueError if boxSize is not in the range (minBoxSize, maxBoxSize).
		"""
		#check boxSize type and range
		if not (isinstance(boxSize, int) and boxSize>=minBoxSize and boxSize<=maxBoxSize):
			raise ValueError
		
		self._value = None
		self._maxValue = boxSize**2
		#preemptive sets the cell belongs to (set after construction by Sudoku class)
		self._linePSet = None
		self._columnPSet = None
		self._boxPSet = None

	def getLinePSet(self):
		"""
		Returns the preemptive set of the cell's line.
		"""
		return self._linePSet

	def getColumnPSet(self):
		"""
		Returns the preemptive set of the cell's column.
		"""
		return self._columnPSet

	def getBoxPSet(self):
		"""
		Returns the preemptive set of the cell's box.
		"""
		return self._boxPSet

	def getPSets(self):
		"""
		Generator returning the preemptive sets of the cell's line, column and box (in this order).
		"""
		yield self.getLinePSet()
		yield self.getColumnPSet()
		yield self.getBoxPSet()

	def setValue(self, value):
		"""
		Sets the value of the cell, and removes value from the free values of the cell's preemptive sets.
		Raises ValueError if value is not in the range (1, tableSize).
		Raises Exception if cell already has a value or if value is not permitted for this cell.
		"""
		#check value type and range
		if not (isinstance(value, int) and value>=1 and value <=self._maxValue):
			raise ValueError
		#check if cell is blank
		if not self.isBlank():
			raise Exception("Cell already has a value")
		#check if value is permitted
		if not self.hasMarkupValue(value):
			raise Exception("Value is not permitted for this cell")
		
		self._value = value
		#remove value from the free values in the preemptive sets the cell belongs to
		for pSet in self.getPSets():
			pSet._freeValues.remove(value)

	def clearValue(self):
		"""
		Clears the value of the cell, and adds value to the free values of the cell's preemptive sets.
		Raises Exception if cell has no value.
		"""
		#check if cell has value
		if self.isBlank():
			raise Exception("Cell has no value")
		
		#add value to the free values in the preemtive sets the cell belongs to
		for pSet in self.getPSets():
			pSet._freeValues.add(self._value)
		self._value = None #make cell blank

	def changeValue(self, value):
		"""
		Clears the cell's value, then sets it to value.
		Same as calling clearValue() then setValue(value)
		"""
		self.clearValue()
		self.setValue(value)

	def isBlank(self):
		"""
		Returns True if the Cell is blank, False otherwise
		"""
		return self._value is None

	def getValue(self):
		"""
		Returns the value contained by the Cell, or None if the Cell is blank.
		"""
		return self._value

	def getMarkupValues(self):
		"""
		Returns a set containing the markup values of the cell.
		"""
		#cell's markup values is the intersection of each of it's preemptive set's free values
		return self._linePSet._freeValues \
			& self._columnPSet._freeValues \
			& self._boxPSet._freeValues

	def hasMarkupValue(self, value):
		"""
		Returns True if value is in the markup values of the cell, False otherwise.
		Raises ValueError if value is not within the range of allowed values.
		"""
		#check value type and range
		if not (isinstance(value, int) and value>=1 and value<=self._maxValue):
			raise ValueError
		
		return value in self.getMarkupValues()

	def getMarkupCount(self):
		"""
		Returns the markup count of the cell (number of markup values).
		"""
		return len(self.getMarkupValues())
		


class Sudoku:
	"""
	Class representing the sudoku table.
	A Sudoku of boxSize n has a tableSize of n**2 and is made of tableSize**2 cells.
	"""

	def __init__(self, boxSize):
		"""
		Creates an instance of Sudoku, with empty cells, of size boxSize**2.
		Raises ValueError if boxSize is not in the range (minBoxSize, maxBoxSize).
		"""
		#check type and range of boxSize
		if not (isinstance(boxSize, int) and boxSize>=minBoxSize and boxSize<=maxBoxSize):
			raise ValueError

		self.boxSize = boxSize #size of one box, in cells
		self.tableSize = boxSize**2 #size of the table, in cells

		#initialize cells with empty Cells
		self._cells = []
		self.clear()
			
	def clear(self):
		"""
		Resets all Cells of the Sudoku, leaving them blank and with full markups.
		"""
		self._cells = [] #clear all of the cells

		#create new cells
		for i in range(self.tableSize):
			cellLine = []
			for j in range(self.tableSize):
				cellLine.append(Cell(self.boxSize))
			self._cells.append(cellLine)

		for index in range(self.tableSize):
			#create new preemptive sets
			lineSet = PreemptiveSet(self.boxSize, self._cells[index][:])
			columnSet = PreemptiveSet(self.boxSize, [self._cells[i][index] \
													for i in range(self.tableSize)])
			topLine, leftColumn = self.getCellCoordsFromBox(index)
			boxSet =  PreemptiveSet(self.boxSize, [self._cells[line][column] \
								for line in range(topLine, topLine+self.boxSize) \
								for column in range(leftColumn, leftColumn+self.boxSize)])
			#assign them to their cells
			for cell in lineSet.getCells():
				cell._linePSet = lineSet
			for cell in columnSet.getCells():
				cell._columnPSet = columnSet
			for cell in boxSet.getCells():
				cell._boxPSet = boxSet
	
	def getBoxIndexFromCell(self, cellLine, cellColumn):
		"""
		Returns the index of the box containing the cell of coordinates (cellLine, cellColumn).
		"""
		return cellColumn//3 + cellLine//3 *3

	def getCellCoordsFromBox(self, boxIndex):
		"""
		Returns the coordinates of the upper left Cell contained in the box of index boxIndex.
		"""
		return ((boxIndex//self.boxSize)%self.boxSize * self.boxSize,
				boxIndex%self.boxSize * self.boxSize)

	def getCell(self, cellLine, cellColumn):
		"""
		Returns the cell located at line cellLine and column cellColumn.
		"""
		#check coordinate's type and range
		if not (isinstance(cellLine, int) and cellLine>=0 and cellLine<self.tableSize):
			raise ValueError
		if not (isinstance(cellColumn, int) and cellColumn>=0 and cellColumn<self.tableSize):
			raise ValueError
		
		return self._cells[cellLine][cellColumn]

	def getCells(self):
		"""
		Generator returning all of the sudoku's cells, from left to right and top to bottom.
		"""
		for cellLine in self._cells:
			for cell in cellLine:
				yield cell
		
	def getLineSet(self, lineIndex):
		"""
		Returns the PreemptiveSet that contains the cells in line index.
		"""
		return self.getCell(lineIndex, 0).getLineSet()

	def getColumnSet(self, columnIndex):
		"""
		Returns the PreemptiveSet that contains the cells in column index.
		"""
		return self.getCell(0, columnIndex).getColumnSet()

	def getBoxSet(self, boxIndex):
		"""
		Returns the PreemptiveSet that contains the cells in box boxIndex.
		"""
		return self.getCell(getCellIndexFromBox(boxIndex)).getBoxSet()

	def getLineSets(self):
		"""
		Generator returning the PreemptiveSet of each line.
		"""
		for i in range(self.tableSize):
			yield self.getLineSet(i)

	def getColumnSets(self):
		"""
		Generator returning the PreemptiveSet of each column.
		"""
		for i in range(self.tableSize):
			yield self.getColumnSet(i)

	def getBoxSets(self):
		"""
		Generator returning the PreemptiveSet of each box.
		"""
		for i in range(self.tableSize):
			yield self.getBoxSet(i)

	def getAllSets(self):
		"""
		Generator returning the PreemptiveSet of each line, column and box (in this order).
		"""
		for line in self.getLineSets():
			yield line
		for column in self.getColumnSets():
			yield column
		for box in self.getBoxSets():
			yield box

	def getCellSets(self, cellLine, cellColumn):
		return self.getCell(cellLine, cellColumn).getSets()

	def isComplete(self):
		for pSet in self.getLineSets():
			if not pSet.isComplete():
				return False
		return True

	def __repr__(self):
		#Separators
		valueMaxWidth = len(str(self.tableSize))
		boxSep = "-" * (valueMaxWidth+2) * self.boxSize
		boxBlank = (" " + ("-"*valueMaxWidth) + " ") * self.boxSize
		
		topBottomSep = "+" + (boxSep + "-")*(self.boxSize-1) + boxSep + "+"
		middleSep = "|" + (boxSep + "+")*(self.boxSize-1) + boxSep + "|"
		blankLine = "|" + (boxBlank + "|") * self.boxSize

		#List of lines
		lineList = []
		lineList.append(topBottomSep)
		for lineIndex in range(self.tableSize):
			#separator for groups of 3 lines
			if lineIndex%self.boxSize==0 and lineIndex!=0: 
				lineList.append(middleSep)
		
			#for each cell of the 
			lineChars = []
			for columnIndex in range(self.tableSize):
				cell = self.getCell(lineIndex, columnIndex)
				if columnIndex%self.boxSize==0: 
					lineChars.append("|")
			
				#display cell's content
				lineChars.append(" ")
				if cell.isBlank():
					lineChars.append("-"*valueMaxWidth)
				else:
					lineChars.append(str(cell.getValue()).rjust(valueMaxWidth))
				lineChars.append(" ")
			lineChars.append("|")
			lineList.append(''.join(lineChars))
		lineList.append(topBottomSep)
		
		return "\n".join(lineList)


#LIBRARY FUNCTIONS

def fillSudokuFromInput(sudoku, safetyClear=False):
	"""
	Fills the sudoku by asking for input via the command line.
	Returns True in case of success, False if the user quits during the process.
	If safetyClear is True, sudoku is cleared if/when the user quits.
	"""

	#print instructions
	blankValue = 0
	print("Use spaces or zeros for blanks, other options are :\n\t- q to quit\n\t- c to clear previous line\n\t- p to print sudoku\n\t- e to end and save sudoku")

	#print header
	inputTextSize = 10
	headerLine = " "*inputTextSize + "".join([str(i+1) for i in range(sudoku.tableSize)]) + "\n" +\
				" "*inputTextSize + "".join(["|" for i in range(sudoku.tableSize)])
	print(headerLine)
	
	lineIndex = 0
	columnOffset = 0
	while lineIndex < sudoku.tableSize:
		#ask for input
		query = "Line " + str(lineIndex + 1) + ": "
		inputText = query + " "*(inputTextSize-len(query)) + "-"*columnOffset
		userInput = input(inputText)

		#if user wants to quit
		if userInput.count("q")>0:
			if safetyClear: #clear sudoku if user quits
				sudoku.clear()
			return False #failure
		
		#if user wants to clear last line
		if userInput.count("c")>0:
			if (lineIndex==0):
				print("No previous line to clear")
			else:
				#clear all cells in last line
				for columnIndex in range(sudoku.tableSize):
					sudoku.clearCellValue(lineIndex, columnIndex)
				lineIndex -= 1
				columnOffset = 0
			continue #start the loop again

		#if user wants to print sudoku
		if userInput.count("p")>0:
			print(sudoku)
			print(headerLine)
			continue
	
		#if user wants to end and save sudoku
		if userInput.count("e")>0:
			return True #success
		
		#if user wants to continue filling the sudoku
		userInput.replace(" ", str(blankValue))
		userInput = str(blankValue)*columnOffset + userInput
	
		#complete the end of the line with blanks if line is too short
		if len(userInput) < sudoku.tableSize:
			userInput += str(blankValue)*(sudoku.tableSize-columnOffset-len(userInput))
	
		#check number and type of values	 
		if not (len(userInput) == sudoku.tableSize and userInput.isdigit()):
			print("Invalid input")
			continue
		
		#try to insert the values in the table
		columnCount=0
		#try:
		for columnIndex in range(sudoku.tableSize):
			columnCount=columnIndex
			value = int(userInput[columnIndex])
			if (value != blankValue):
				sudoku.getCell(lineIndex, columnIndex).setValue(value)
		"""except Exception as e:
			print("Error when inserting in column " + str(columnCount+1) + ":")
			print(e)
			columnOffset = columnCount
		else:
			lineIndex += 1
			columnOffset = 0"""

	return True #success

