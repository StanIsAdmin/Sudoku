from sudoku import *

sudo = Sudoku(4)
print(sudo.getCell(0,0).getMarkupValues())
fillSudokuFromInput(sudo)
print(sudo)
			
