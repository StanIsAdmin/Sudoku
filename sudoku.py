"""
A library designed to create, display (command line) and solve sudoku puzzles.
"""

#Allowed sizes for the sudoku's boxes
minBoxSize=2
maxBoxSize=8

#Allowed sizes for the sudoku's table
minTableSize=minBoxSize**2
maxTableSize=maxBoxSize**2

class Cell:
	"""
	Class representing a cell of the sudoku table.
	A Cell is either Blank or has a Value, that can range from 1 to the sudoku's tableSize.
	A Cell contains markup values, which are the values it can hold without violating the sudoku rules.
	"""

	self.blankValue = 0

	def __init__(self, boxSize):
		"""
		Creates an instance of Cell allowing values in the range (1, boxSize**2).
		Upon construction, the markup values of the Cell consist of all of the possible values, and the Cell itself is left Blank.
		Raises ValueError if boxSize is not in the range (minBoxSize, maxBoxSize).
		"""
		#check value type and range
		if not (isinstance(boxSize, int) and boxSize>=minBoxSize and boxSize<=maxBoxSize):
			raise ValueError

		tableSize=boxSize**2 #size of the table
		self.value = self.blankValue

		#list of possible values (>0 when possible), where value is index+1
		#3 means none of pSets containing the cell have the set the value (value is free)
		#0,1,2 mean the value can not be set for the cell but may be for 0,1,2 of it's pSets
		self.markupValues = [3 for i in range(tableSize)]
		self.markupCount = tableSize #number of possible values

	def __setValue__(self, value):
		"""
		PRIVATE METHOD. SUDOKU INTEGRITY NOT GUARANTEED.
		Sets the value of the cell.
		Raises ValueError if value is not in the range (1, tableSize).
		Raises Exception if cell already has a value.
		"""
		#check value type and range
		if not (isinstance(value, int) and value>0 and value <=len(self.markupValues)):
			raise ValueError
		#check if cell is blank
		if not self.isBlank():
			raise Exception("Cell already has a value")
		
		self.value = value

	def __clearValue__(self):
		"""
		PRIVATE METHOD. SUDOKU INTEGRITY NOT GUARANTEED.
		Clears the value of the cell.
		Raises Exception if cell has no value.
		"""
		#check if cell has value
		if self.isBlank():
			raise Exception("Cell has no value")
		
		self.value = blankValue
		
	def __addMarkupValue__(self, value):
		"""
		PRIVATE METHOD. SUDOKU INTEGRITY NOT GUARANTEED.
		Adds value to the markup values of the cell.
		Raises ValueError if value is not in the range (1, tableSize).
		Raises Exception if value is already in markup values for the 3 preemptive sets containing the cell.
		"""
		#check value type and range
		if not (isinstance(value, int) and value>0 and value<=len(self.markupValues)):
			raise ValueError
		#check if value is not already in markup for all 3 preemptive sets
		if self.markupValues[value-1]==3:
			raise Exception("Value already in markup for all preemptive sets")

		#add value to one of the preemptive set's markup
		self.markupValues[value-1] += 1

		#if value is not in markup for all pSets
		if self.hasMarkupValue(value):
			self.markupCount += 1 #increase markup count

	def __removeMarkupValue__(self, value):
		"""
		PRIVATE METHOD. SUDOKU INTEGRITY NOT GUARANTEED.
		Removes value from the markup values of the cell.
		Raises Exception if no markup value remain for the cell.
		Returns True if only one markup value remains, False otherwise.
		"""
		#check value type and range
		if not (isinstance(value, int) and value>0 and value<=len(self.markupValues)):
			raise ValueError
		#check if value is at least in markup for one preemptive set
		if self.markupValues[value-1]==0:
			raise Exception("Value is not in markup for any preemptive set")
		#check if value was the last possible value for this cell
		if self.markupCount==1 and not self.isBlank() and self.markupValues[value-1]==1:
			raise Exception("No remaining possible values for cell") #sudoku has no solution

		#if value was in markup for all pSets
		if self.hasMarkupValue(value):
			self.markupCount -= 1 #decrease markup count
		
		#remove value for one of the preemptive set's markup
		self.markupValues[value-1] -= 1

		#if only one possible value remains, it should become the cell's value
		if self.markupCount == 1:
			return True
		else:
			return False

	def isBlank(self):
		"""
		Returns True if the Cell is blank, False otherwise
		"""
		return self.value == blankValue

	def getValue(self):
		"""
		Returns the value contained by the Cell.
		"""
		return self.value

	def getMarkupCount(self):
		"""
		Returns the markup count of the cell (number of possible values).
		"""
		return self.markupCount

	def getMarkupValues(self):
		"""
		Generator returning the markup values of the cell.
		"""
		for i in range(len(self.markupValues)):
			#if value is in markup for all pSets (value is possible for cell)
			if self.markupValues[i]==3:
				yield i+1

	def hasMarkupValue(self, value):
		"""
		Returns True if value is in the markup values of the cell, False otherwise.
		Raises ValueError if value is not within the range of allowed values.
		"""
		#check value type and range
		if not (isinstance(value, int) and value>0 and value<=len(self.markupValues)):
			raise ValueError
		
		return self.markupValues[value-1]==3
				

class PreemptiveSet:
	"""
	A preemptive set is a list of m values, each of them between 1 and m, together with a list of m cells, with the property that no values other than the m values from the list can occupy the m cells. 
	Here we consider a cell with the value blankValue as an empty cell.
	"""

	def __init__(self, boxSize, cellList):
		"""
		Creates an instance of PreemptiveSet with the list of cells cellList.
		Raises ValueError if boxSize is not in the range (minBoxSize, maxBoxSize) or if cellList is not a list of boxSize**2 Cells.
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
		
		self.cells = cellList #preemptive set's cells

	def getCells(self):
		"""
		Genereator returning the preemptive set's cells.
		"""
		for cell in self.cells:
			yield cell
	
	def hasSetValue(self, value):
		"""
		Returns True if one of the Cells has value as its value, False otherwise.
		Raises ValueError if value is not in the range (1, boxSize**2)
		"""
		#check value 
		if not (isinstance(value, int) and value>0 and value <=len(self.cells)):
			raise ValueError
		
		#for each cell value
		for cell in self.cells:
			if value == cell.getValue(): #if it's the value we look for
				return True
			
		return False
	
	def isComplete(self):
		"""
		Returns True if each cell of the preemptive set's values is in exactly one cell.
		"""
		#for each cell
		for cell in self.cells:
			if cell.isBlank(): #if the cell is blank
				return False

		return True
		

class Sudoku:
	"""
	Class representing the sudoku table.
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

		#initialize cellTable with empty Cells
		self.cellTable = []
		self.clear()
			
	def clear(self):
		"""
		Resets all Cells of the Sudoku, leaving them blank and with full markups.
		"""
		self.cellTable = []
		for line in range(self.boxSize**2):
			cellLine = []
			for column in range(self.boxSize**2):
				cellLine.append(Cell(self.boxSize))
			self.cellTable.append(cellLine)

	def getCell(self, cellLine, cellColumn):
		"""
		Returns the cell located at line cellLine and column cellColumn.
		"""
		#check coordinate's type and range
		if not (isinstance(cellLine, int) and cellLine>=0 and cellLine<self.tableSize):
			raise ValueError
		if not (isinstance(cellColumn, int) and cellColumn>=0 and cellColumn<self.tableSize):
			raise ValueError
		
		return self.cellTable[cellLine][cellColumn]

	def getCells(self):
		"""
		Generator returning all cells of the table.
		"""
		for cellLine in self.cellTable:
			for cell in cellLine:
				yield cell

	def setCellValue(self, cellLine, cellColumn, value):
		"""
		Sets the value of the cell located at line cellLine and column cellColumn.
		Removes the value from the markup of all of the cells belonging in any of this cell's preemptive sets.
		Raises ValueError if coordinates are not valid (as defined in getCell) or if value is not in the range (1, tableSize).
		Raises Exception is cell already has a value or if value is not available for the cell.
		"""
		#check type and range of coordinates
		cell = self.getCell(cellLine, cellColumn)
		#check type and range of value
		if not (isinstance(value, int) and value>0 and value <=self.tableSize):
			raise ValueError
		#check if cell is blank
		if not cell.isBlank():
			raise Exception("Cell already contains a value")
		#check if value is available for this cell
		if not cell.hasMarkupValue(value):
			raise Exception("Value is already contained in one of the cell's preemptive sets")

		#remove value from the pset's markup values
		for pSet in self.getCellSets(cellLine, cellColumn):
			for pSetCell in pSet.getCells():
				pSetCell.__removeMarkupValue__(value)
		
		#actually set the cell value (Sudoku if a "friend" class for Cell)
		cell.__setValue__(value)
	
	def clearCellValue(self, cellLine, cellColumn):
		"""
		Clears the value of the cell located at line cellLine and column cellColumn.
		Adds the value to the markup values of the cells belonging in any of this cell's preemptive sets whenever the value is not already in any of these cell's other preemptive sets.
		Raises ValueError if coordinates are not valid (as defined in getCell).
		"""
		#check type and range of coordinates
		cell = self.getCell(cellLine, cellColumn)

		#if cell has a value
		if not cell.isBlank():
			value = cell.getValue()
			#add value to the pset's markup values
			for pSet in self.getCellSets(cellLine, cellColumn):
				for pSetCell in pSet.getCells():
					pSetCell.__addMarkupValue__(value)
			
			#clear the cell value
			cell.__clearValue__()

	def changeCellValue(self, cellLine, cellColumn, value):
		self.clearCellValue(cellLine, cellColumn)
		self.setCellValue(cellLine, cellColumn, value)

	def getBoxIndexFromCell(self, cellLine, cellColumn):
		return cellColumn//3 + cellLine//3 *3

	def getLineSet(self, lineIndex):
		return PreemptiveSet(self.boxSize, self.cellTable[lineIndex][:])

	def getColumnSet(self, columnIndex):
		return PreemptiveSet(self.boxSize, [self.cellTable[i][columnIndex] for i in range(9)])

	def getBoxSet(self, boxIndex):
		topLine = (boxIndex//3)%3 *3
		leftColumn = boxIndex%3 *3
		return PreemptiveSet(self.boxSize, [self.cellTable[line][column] \
							for line in range(topLine, topLine+self.boxSize) \
							for column in range(leftColumn, leftColumn+self.boxSize)])

	def getLineSets(self):
		for i in range(self.tableSize):
			yield self.getLineSet(i)

	def getColumnSets(self):
		for i in range(self.tableSize):
			yield self.getColumn(i)

	def getBoxSets(self):
		for i in range(self.tableSize):
			yield self.getBox(i)

	def getAllSets(self):
		for line in self.getLines():
			yield line
		for column in self.getColumns():
			yield column
		for box in self.getBoxes():
			yield box

	def getCellSets(self, cellLine, cellColumn):
		yield self.getLineSet(cellLine)
		yield self.getColumnSet(cellColumn)
		yield self.getBoxSet(self.getBoxIndexFromCell(cellLine, cellColumn))

	def isComplete(self):
		for pSet in self.getLineSets():
			if not pSet.isComplete():
				return False
		return True

	def __repr__(self):
		#Separators
		boxSep = "---" * self.boxSize
		boxBlank = " - " * self.boxSize
		
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
		
			#blank line
			lineChars = list(blankLine)

			#fill the blanks		
			for columnIndex in range(self.tableSize):
					#position of the value in the line
					offset = 2 + (columnIndex*self.boxSize) + (columnIndex//self.boxSize)
					cell = self.getCell(lineIndex, columnIndex)
					#if the cell isn't blank, display its value
					if not cell.isBlank():
						lineChars[offset] = str(cell.getValue())
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
	print("Use spaces or 0 for blanks, other options are :\n\t- q to quit\n\t- c to clear previous line\n\t- p to print sudoku\n\t- e to end and save sudoku")

	#print header
	inputTextSize = 12
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
		try:
			for columnIndex in range(sudoku.tableSize):
				columnCount=columnIndex
				value = int(userInput[columnIndex])
				if (value != blankValue):
					sudoku.setCellValue(lineIndex, columnIndex, value)
		except Exception as e:
			print("Error when inserting in column " + str(columnCount+1) + ":")
			print(e)
			columnOffset = columnCount
		else:
			lineIndex += 1
			columnOffset = 0

	return True #success

