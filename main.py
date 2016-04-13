from sudoku import *

sudo = Sudoku(8)
print(sudo.getCell(0,0).getMarkupValues())
fillSudokuFromInput(sudo)
print(sudo)
