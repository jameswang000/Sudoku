#Extra Features
#1. Autoplayed Singletons and other Hints
#2. Clean UI
#3. Better Hint Generator (X Wing Hint) (Challenging Feature)
#4. A clock

import sys, os

#3 functions below taken from Sudoku Overview page.
#https://www.cs.cmu.edu/afs/cs.cmu.edu/academic/
#class/15112-3-s23/www/notes/term-project.html

#####################
# Set Up
#####################

def runPipCommand(pipCommand, pipPackage=None):
    # get quoted executable path
    quote = '"' if 'win' in sys.platform else "'"
    executablePath = f'{quote}{sys.executable}{quote}'
    # first upgrade pip:
    command = f'{executablePath} -m pip -q install --upgrade pip'
    os.system(command)
    # input the package from the user if it's not supplied in the call:
    if pipPackage == None:
        pipPackage = input(f'Enter the pip package for {pipCommand} --> ')
    # then run pip command:
    command = f'{executablePath} -m pip {pipCommand} {pipPackage}'
    os.system(command)

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

#Use this to access the boards folder whenever you need something from it.
path = "./tp-starter-files\\boards"

######################
# APP BELOW HERE
######################

#Graphics Engine from CMU Graphics:
#https://academy.cs.cmu.edu/desktop
from cmu_graphics import *
import random
import copy
import itertools

######################
# Helper Functions 
######################

def intersectingRect(rectLeft, rectTop, width, height, mouseX, mouseY):
    rectRight = rectLeft + width
    rectBot = rectTop + height
    return (rectLeft <= mouseX <= rectRight) and (rectTop <= mouseY <= rectBot)

######################
# Inital Screen
######################

def initial_onAppStart(app):
    app.playButtonLeft = 300
    app.playButtonTop = 550
    app.playButtonWidth = 200
    app.playButtonHeight = 100

def initial_redrawAll(app):
    #background color
    drawRect(0, 0, app.width, app.height, 
             fill='lightGreen', border='brown', borderWidth=3) 
    initial_drawTitle(app)
    initial_drawPlayButton(app)

def initial_drawTitle(app):
    cx, cy = 400, 200
    drawRect(cx, cy, 400, 200, fill='lightPink', border='black', align='center')
    drawLabel('Cactus Sudoku', cx, cy, size=50, bold=True)
    drawOval(app.width/2, app.height/2 + 10, 50, 150, 
             fill='green', border='black')
    drawOval(app.width/2 + 35, app.height/2 - 20, 25, 75, 
             rotateAngle=10, fill='green', border='black')
    drawOval(app.width/2 - 35, app.height/2 - 20, 25, 60, 
             rotateAngle=-10, fill='green', border='black')
    drawCircle(app.width/2 + 10, app.height/2 - 20, 5, fill='black')
    drawCircle(app.width/2 - 10, app.height/2 - 20, 5, fill='black')
    drawOval(app.width/2, app.height/2 + 30, 15, 50, 
             fill='black')


def initial_drawPlayButton(app):
    cx = app.playButtonLeft + app.playButtonWidth/2
    cy = app.playButtonTop + app.playButtonHeight/2
    drawRect(cx, cy, 200, 100, fill='red', border='black', align='center')
    drawLabel('Play', cx, cy, size=60, bold=True)

def initial_onMousePress(app, mouseX, mouseY):
    if intersectingRect(app.playButtonLeft, app.playButtonTop, 
                                app.playButtonWidth, app.playButtonHeight,
                                mouseX, mouseY):
        setActiveScreen('help') 
    
###################### 
# Help Screen 
######################

def help_onAppStart(app):
    app.difficulties = ['easy', 'medium', 'hard', 'expert', 'evil']
    
    app.buttonLeft = 125
    app.buttonTop = 600
    app.buttonWidth = 100
    app.buttonHeight = 50

    app.currentDifficulty = None

def help_redrawAll(app):
    drawRect(0, 0, app.width, app.height, 
             fill='lightGreen', border='brown', borderWidth=3)
    drawInstructions(app)
    help_drawButton(app)

def drawInstructions(app):
    fontSize = 20
    drawLabel('Welcome to Sudoku!', app.width/2, 200, size=fontSize)
    drawLabel('Fill all empty squares with legal values to win.', 
              app.width/2, 225, size=fontSize)
    instructions = ('Every row, col, and 3x3 block ' +
                    'must contain each number from 1-9 only once.')
    drawLabel(instructions, app.width/2, 250, size=fontSize)
    instructions = ('Click an empty or black numbered cell, ' + 
                    'then press a number from 1 to 9 to fill in a cell.')
    drawLabel(instructions, app.width/2, 275, size=fontSize)
    drawLabel('Press n to get a new board.', app.width/2, 300, size=fontSize)
    drawLabel('Press l to disable/enable legals display.', 
              app.width/2, 325, size=fontSize)
    drawLabel('Press h to hightlight a hint', app.width/2, 350, size=fontSize)
    drawLabel('Press s to play a hint', app.width/2, 375, size=fontSize)
    drawLabel('Press a to enable automode', app.width/2, 400, size=fontSize)
    drawLabel('Click a difficulty to begin', app.width/2, 425, size=fontSize)

def help_drawButton(app):
    for i in range(len(app.difficulties)):
        rectLeft = app.buttonLeft + i * (app.buttonWidth + 12.5) 
        rectTop = app.buttonTop
        cx = rectLeft + app.buttonWidth/2
        cy = rectTop + app.buttonHeight/2
        drawRect(rectLeft, rectTop, app.buttonWidth, app.buttonHeight, 
                 fill='red', border='black')
        drawLabel(app.difficulties[i].upper(), cx, cy, size=20, bold=True)

def help_onMousePress(app, mouseX, mouseY):
    for i in range(len(app.difficulties)):
        rectLeft = app.buttonLeft + i * (app.buttonWidth + 12.5) 
        rectTop = app.buttonTop
        #Sets app.difficulties to prepare for play screen set up
        if intersectingRect(rectLeft, rectTop, app.buttonWidth, 
                            app.buttonHeight, mouseX, mouseY):
            difficulty = app.difficulties[i]
            app.currentDifficulty = difficulty
            setActiveScreen('play')
            

######################
# Play Screen
######################

#Sets up some unchanging values 
def play_onAppStart(app):
    #Sets the parameter for the physical board
    app.rows = 9
    app.cols = 9
    app.boardLeft = 175
    app.boardTop = 50
    app.boardWidth = 450
    app.boardHeight = 450
    app.cellBorderWidth = 1
    
    #Initializes location of back button
    app.backButtonLeft = 300
    app.backButtonTop = 550
    app.backButtonWidth = 200
    app.backButtonHeight = 100

    #Initializes a list of boards for each difficulty
    getAllBoards(app)

    #Sets the step speed
    app.stepsPerSecond = 10

#Sets current board to a random board of appropriate difficulty when
#A difficulty is selected from the help screen
def play_onScreenActivate(app):
    play_restart(app)

#Resets all gameplay variables
def play_restart(app):
    if app.currentDifficulty == 'easy':
        boardText = random.choice(app.easyBoards)
    elif app.currentDifficulty == 'medium':
        boardText = random.choice(app.mediumBoards)
    elif app.currentDifficulty == 'hard':
        boardText = random.choice(app.hardBoards)
    elif app.currentDifficulty == 'expert':
        boardText = random.choice(app.expertBoards)
    elif app.currentDifficulty == 'evil':
        boardText = random.choice(app.evilBoards)
    else:
        boardText = ''
    
    #Creates an initial board and one to modify to get the solution
    app.board = getBoardFromText(boardText)
    boardRecord = copy.deepcopy(app.board)
    
    #Handles all of the game state variables here
    setGameStateVars(app)
    #Initializes each cell's legal values
    app.legalsBoard = []
    for row in range(app.rows):
        rowList = []
        for col in range(app.cols):
            rowList.append({1, 2, 3, 4, 5, 6, 7, 8, 9})
        app.legalsBoard.append(rowList)
    
    #Updates legals based on initial filled in values.
    setLegals(app)
    app.legalModeOn = True
    app.autoModeOn = False
    app.steps = 0

    #Obtains the solution to the specific puzzle
    app.solutionBoard = getSolution(app, app.board)
    #Since the solver works on the actual board, the actual board is restored
    #to its inital state after the solver runs.
    app.board = boardRecord 
    setLegals(app)
    app.gameOver = False

def setGameStateVars(app):
    app.hintedCells = set()
    app.selected = None
    app.isHardSelected = False
    app.selectedRegions = set()
    app.regions = [[] for i in range(28)]
    setRegions(app)
    app.bannedLegals = set()
    app.obviousTupleHintedCells = set()
    app.xWingRowHintedCells = set()
    app.xWingColHintedCells = set()
    app.xWingModeOn = False

#Inspiration taken from 8.11 solveMiniSudoku
#https://cs3-112-f22.academy.cs.cmu.edu/exercise/4823

def getSolution(app, board):
    if findLeastLegals(app, board) == None:
        #Solved when no legal values exist anywhere
        return board
    else:
        row, col = findLeastLegals(app, board)
        #Tries solving after placing every possible legal in a cell
        #Backtracks when a cell has no legals remaining, which would eventually
        #happen if a wrong number is placed in a cell since Sudokus only have 
        #one valid solution.
        for num in app.legalsBoard[row][col]:
            board[row][col] = num
            setLegals(app)
            solution = getSolution(app, board)
            if solution != None:
                return solution
            board[row][col] = 0
            setLegals(app)
        None

#Finds the cell with the fewest unique legal values.
def findLeastLegals(app, board):
    leastLegalsCell = None
    leastLegals = 10
    for row in range(app.rows):
        for col in range(app.cols):
            if board[row][col] == 0:
                cellLegals = app.legalsBoard[row][col]
                legalCount = len(cellLegals)
                if legalCount < leastLegals:
                    leastLegalsCell = (row, col)
                    leastLegals = legalCount
    return leastLegalsCell

#Regions format taken from Sudoku hints on Sudoku overview
#https://www.cs.cmu.edu/afs/cs.cmu.edu/academic/class/
#15112-3-s23/www/notes/tp-sudoku-hints.html    

def setRegions(app):
    for row in range(app.rows):
        for col in range(app.cols):
            currentCell = (row, col)
            #Adds to correct row region
            app.regions[row].append(currentCell)
            #Adds to correct col region
            app.regions[col + 9].append(currentCell)

            #Adds to correct block region
            #4.5 isLegalSudoku adapted for blocks format
            #https://cs3-112-f22.academy.cs.cmu.edu/exercise/4745
            startRow = row//3
            startCol = col//3
            app.regions[startRow * 3 + startCol + 18].append(currentCell)
    #The first 9 sublists in regions is rows, the next 9 sublists are cols,
    #and the final 9 sublists in  regions is blocks. Hence the +9 and + 18.

def setLegals(app):
    for row in range(app.rows):
        for col in range(app.cols):
            #Always sets a cell's legal to all values then removes values
            #based on board state.
            currentCell = (row, col)
            app.legalsBoard[row][col] = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            #Interates through each region the current cell is found in 
            #and for each other cell not equal to the current cell, eliminate 
            #its legals from the currentcell.
            for region in app.regions:
                if currentCell in region:
                    for otherRow, otherCol in region:
                        if (row, col) != (otherRow, otherCol):
                            removeLegal(app, currentCell, otherRow, otherCol)
    #Removes banned legals from previous hints from all cells.
    for bannedTuple in app.bannedLegals:
        row, col, bannedLegal = bannedTuple
        if bannedLegal in app.legalsBoard[row][col]:
            app.legalsBoard[row][col].remove(bannedLegal)
    
def removeLegal(app, currentCell, otherRow, otherCol):
    row, col = currentCell
    currentCellLegals = app.legalsBoard[row][col]
    otherCellContent = abs(int(app.board[otherRow][otherCol]))
    if otherCellContent != 0 and otherCellContent in currentCellLegals:
        currentCellLegals.remove(otherCellContent)
                            
def getBoardFromText(boardText):
    result = []
    for line in boardText.splitlines():
        rowList = []
        for numStr in line.split(' '):
            rowList.append(int(numStr))
        result.append(rowList)
    return result

def getAllBoards(app):
    app.easyBoards   = []
    app.mediumBoards = []
    app.hardBoards   = []
    app.expertBoards = []
    app.evilBoards   = []
    for filename in os.listdir(path):
        if filename.endswith('.txt'):
            pathToFile = f'{path}\\{filename}'
            fileContents = readFile(pathToFile)
            if 'easy' in filename:
                app.easyBoards.append(fileContents)
            elif 'medium' in filename:
                app.mediumBoards.append(fileContents)
            elif 'hard' in filename:
                app.hardBoards.append(fileContents)
            elif 'expert' in filename:
                app.expertBoards.append(fileContents)
            elif 'evil' in filename:
                app.evilBoards.append(fileContents)

#Checks for whether the Sudoku is solved based on similarity to solution board
#Also resets cell selections whenever its called after the game is won.
def checkGameState(app):
    for row in range(app.rows):
        for col in range(app.cols):
            if abs(app.board[row][col]) != app.solutionBoard[row][col]:
                return
    app.gameOver = True
    app.selected = None
    app.isHardSelected = False
    app.selectedRegions = set()

#Checks whether there is any wrong values to prevent hints from acting based on
#Incorrect board states and permenantly removing legal.
#Hints can only be called on correct current board states.
def isBoardWrong(app):
    for row in range(app.rows):
        for col in range(app.cols):
            cellContent = app.board[row][col]
            if (abs(cellContent) != app.solutionBoard[row][col] and
                cellContent != 0):
                return True
    return False

#Checks for the appearence of each type of hint in the order of obviousSingle
#Obvious tuple, and XWing. Only highlights one hint for each press 
#and highlight remains until the hint is executed. 
#The hints are structured to only see what a play can see, it acts based on 
#visible legals only.

#Deals with the issue of useless hints using recursion for both highlight and 
#change board hints. Checks if the hint will alter any visible cells and 
#keep calling it until something is altered.

def highlightHintedCell(app):
    #Handles obviousSingleHint
    app.hintedCells = set()
    if not app.xWingModeOn:
        obviousSingle = findObviousSingle(app)
        if obviousSingle != None:
            app.hintedCells = {obviousSingle}
            return

        #Handles obviousTupleHint
        obviousTuple = findObviousTuple(app)
        if obviousTuple != None:
            for row, col in obviousTuple:
                app.hintedCells.add((row, col))
            newBannedLegals = getBannedObviousTupleLegals(app, obviousTuple)
            if bansAreUseless(app, newBannedLegals):
                app.obviousTupleHintedCells.add(obviousTuple)
                for ban in newBannedLegals:
                    app.bannedLegals.add(ban)
                highlightHintedCell(app)
            return 
    
    #Handles X Wing Hint
    rowXWingTuple = findRowXWingTuple(app)
    colXWingTuple = findColXWingTuple(app)
    if rowXWingTuple != None:
        xWingTuple = rowXWingTuple
        newBannedLegals = getRowXWingTupleBans(app, xWingTuple)
        xWingType = 'row'
    elif colXWingTuple != None:
        xWingTuple = colXWingTuple
        newBannedLegals = getColXWingTupleBans(app, xWingTuple)
        xWingType = 'col'
    else:
        xWingTuple = None

    if xWingTuple != None:
        for i in range(1, len(xWingTuple)):
            row, col = xWingTuple[i]
            app.hintedCells.add((row, col))
        
        if bansAreUseless(app, newBannedLegals):
            if xWingType == 'row':
                app.xWingRowHintedCells.add(xWingTuple)
            else:
                app.xWingColHintedCells.add(xWingTuple)
            for ban in newBannedLegals:
                app.bannedLegals.add(ban)
            highlightHintedCell(app)

#Changes the cell content or bans specific values.
#Hint structure: Tries to find cells with that hint and changes values only if 
#something is actually found.

def changeHintedCell(app):
    # Handles the singleton hint
    if not app.xWingModeOn:
        obviousSingle = findObviousSingle(app)
        if obviousSingle != None:
            row, col = obviousSingle
            currentLegals = app.legalsBoard[row][col]
            #Since obvious singles only have one legal, that legal is what the 
            #cell's content should be set to.
            for i in range(1, 10):
                if i in currentLegals:
                    onlyLegal = i
            #Alterable cells are stored with either a 0 or negative number
            #Compared to given cells which are represented by positive numbers
            app.board[row][col] = onlyLegal * -1
            #Removed highlight once the hint is played.
            app.hintedCells = set()
            #Since this hint changes the board state, we must update legals and
            #check whether the game is over.
            checkGameState(app)
            return
        
        #Handles the tuple hint
        obviousTuple = findObviousTuple(app)
        if obviousTuple != None:
            newBannedLegals = getBannedObviousTupleLegals(app, obviousTuple)
            app.obviousTupleHintedCells.add(obviousTuple)
            for ban in newBannedLegals:
                app.bannedLegals.add(ban)
            #Banned legals are added to a set of banned tuple
            if bansAreUseless(app, newBannedLegals):
                changeHintedCell(app)
            return
    
    #Handles the X Wing Hint in two cases: row and col
    rowXWingTuple = findRowXWingTuple(app)
    if rowXWingTuple != None:
        app.xWingRowHintedCells.add(rowXWingTuple)
        newBannedLegals = getRowXWingTupleBans(app, rowXWingTuple)
        for ban in newBannedLegals:
            app.bannedLegals.add(ban)
        if bansAreUseless(app, newBannedLegals):
            changeHintedCell(app)
        return
    
    colXWingTuple = findColXWingTuple(app)
    if colXWingTuple != None:
        app.xWingColHintedCells.add(colXWingTuple)
        newBannedLegals = getColXWingTupleBans(app, colXWingTuple)
        for ban in newBannedLegals:
            app.bannedLegals.add(ban)
        if bansAreUseless(app, newBannedLegals):
            changeHintedCell(app)
        return
    return 'No Hints Left'

def bansAreUseless(app, newBannedLegals):
    for row, col, legal in newBannedLegals:
        if app.board[row][col] == 0 and legal in app.legalsBoard[row][col]:
            return False
    return True

#XWing Hint Idea from:
#https://www.sudokuonline.io/tips/advanced-sudoku-strategies +
#https://www.youtube.com/watch?v=ooMuXjuOF1E&ab_channel=LearnSomething

#XWing Hint Helper Functions
def findRowXWingTuple(app):
    rowsDoubleOccurences = dict()
    for row in range(app.rows):
        rowLegalOccurences = getRowLegalOccurences(app, row)
        for legal in rowLegalOccurences:
            if len(rowLegalOccurences[legal]) == 2:
                cell1, cell2 = tuple(rowLegalOccurences[legal])
                row1, col1 = cell1
                row2, col2 = cell2
                s = rowsDoubleOccurences.get(row, set())
                s.add((str(legal), col1, col2))
                rowsDoubleOccurences[row] = s
    for row in rowsDoubleOccurences:
        for doubleOccurence in rowsDoubleOccurences[row]:
            for otherRow in rowsDoubleOccurences:
                if otherRow != row:
                    for otherDoubleOccurence in rowsDoubleOccurences[otherRow]:
                        s1 = set(doubleOccurence)
                        s2 = set(otherDoubleOccurence)
                        if s1 == s2:
                            legal, col1, col2 = doubleOccurence
                            legal = int(legal)
                            result = (legal, (row, col1), (row, col2),
                                      (otherRow, col1), (otherRow, col2))
                            if (result not in app.xWingRowHintedCells and
                                cornersAreLegal(app, result) and
                                getRowXWingTupleBans(app, result) != []):
                                return result

def getRowLegalOccurences(app, row):
    legalOccurences = dict()
    for col in range(app.cols):
        if app.board[row][col] == 0: 
            currentLegals = app.legalsBoard[row][col]
            for legal in currentLegals:
                s = legalOccurences.get(legal, set())
                s.add((row, col))
                legalOccurences[legal] = s
    return legalOccurences

def getRowXWingTupleBans(app, xWingTuple):
    bannedLegals = []
    legal, cell1, cell2, cell3, cell4 = xWingTuple
    row1, col1 = cell1
    row3, col3 = cell4
    for row in range(app.rows):
        if row != row1 and row != row3:
            bannedLegals.append((row, col1, legal))
            bannedLegals.append((row, col3, legal))
    return bannedLegals

def findColXWingTuple(app):
    colsDoubleOccurences = dict()
    for col in range(app.cols):
        colLegalOccurences = getColLegalOccurences(app, col)
        for legal in colLegalOccurences:
            if len(colLegalOccurences[legal]) == 2:
                cell1, cell2 = tuple(colLegalOccurences[legal])
                row1, col1 = cell1
                row2, col2 = cell2
                s = colsDoubleOccurences.get(col, set())
                s.add((str(legal), row1, row2))
                colsDoubleOccurences[col] = s
    for col in colsDoubleOccurences:
        for doubleOccurence in colsDoubleOccurences[col]:
            for otherCol in colsDoubleOccurences:
                if otherCol != col:
                    for otherDoubleOccurence in colsDoubleOccurences[otherCol]:
                        s1 = set(doubleOccurence)
                        s2 = set(otherDoubleOccurence)
                        if s1 == s2:
                            legal, row1, row2 = doubleOccurence
                            legal = int(legal)
                            result = (legal, (row1, col), (row2, col),
                                      (row1, otherCol), (row2, otherCol))
                            if (result not in app.xWingColHintedCells and
                                cornersAreLegal(app, result) and
                                getColXWingTupleBans(app, result) != []):
                                return result

def getColLegalOccurences(app, col):
    legalOccurences = dict()
    for row in range(app.rows):
        if app.board[row][col] == 0: 
            currentLegals = app.legalsBoard[row][col]
            for legal in currentLegals:
                s = legalOccurences.get(legal, set())
                s.add((row, col))
                legalOccurences[legal] = s
    return legalOccurences

def getColXWingTupleBans(app, xWingTuple): 
    bannedLegals = []
    legal, cell1, cell2, cell3, cell4 = xWingTuple
    row1, col1 = cell1
    row3, col3 = cell4
    for col in range(app.cols):
        if col != col1 and col != col3:
            bannedLegals.append((row1, col, legal))
            bannedLegals.append((row3, col, legal))
    return bannedLegals

def cornersAreLegal(app, potentialXWingtuple):
    for i in range(1, len(potentialXWingtuple)):
        row, col = potentialXWingtuple[i]
        if app.board[row][col] != 0:
            return False
    return True

#Obvious Tuple Hint Helper Functions
def getBannedObviousTupleLegals(app, obviousTuple):
    newBannedLegals = []
    obviousTupleLegals = getObviousTupleLegals(app, obviousTuple)
    for region in app.regions:
            if containsObviousTuple(region, obviousTuple):
                for row, col in region:
                    if (row, col) not in obviousTuple:
                        for legal in obviousTupleLegals:
                            newBannedLegals.append((row, col, legal))
    return newBannedLegals
                        
def getObviousTupleLegals(app, obviousTuple):
    s = set()
    for row, col in obviousTuple:
        s = s | app.legalsBoard[row][col]
    return s

def containsObviousTuple(region, obviousTuple):
    for cell in obviousTuple:
        if cell not in region:
            return False
    return True

#Below two functions inspiration from Term Project Hint 2 Overview
#https://www.cs.cmu.edu/afs/cs.cmu.edu/academic/
#class/15112-3-s23/www/notes/term-project.html

def findObviousTuple(app):
    for N in range(2, 6):
        for region in app.regions:
            for possObviousTuple in itertools.combinations(region, N):
                if (possObviousTuple not in app.obviousTupleHintedCells and 
                    isObviousTuple(app, possObviousTuple, N)):
                    if getBannedObviousTupleLegals(app, possObviousTuple) != []:
                        return possObviousTuple
    return None

def isObviousTuple(app, possibleObviousTuple, N):
    s = set()
    for row, col in possibleObviousTuple:
        if app.board[row][col] != 0: return False
        if len(app.legalsBoard[row][col]) == 1: return False
        s = s | app.legalsBoard[row][col]
    if len(s) == N:
        return True
    else:
        return False

#Obvious single hint helper function
def findObviousSingle(app):
    for row in range(app.rows):
        for col in range(app.cols):
            if app.board[row][col] == 0: 
                currentLegals = app.legalsBoard[row][col]
                if len(currentLegals) == 1:
                    return (row, col)

#Controller Functions for play screen below here
def play_onKeyPress(app, key):
    if key == 'n':
        play_restart(app) 
    elif key.isdigit() and app.isHardSelected and app.gameOver == False:
        row, col = app.selected
        app.board[row][col] = int(key) * -1
        if (row, col) in app.hintedCells:
            app.hintedCells.remove((row, col))
        setLegals(app)
        checkGameState(app)
    elif key == 'l' and app.gameOver == False:
        app.legalModeOn = not app.legalModeOn
    elif key == 'h' and app.gameOver == False and not isBoardWrong(app):
        highlightHintedCell(app)
    elif key == 's' and app.gameOver == False and not isBoardWrong(app):
        changeHintedCell(app)
        setLegals(app)
    elif key == 'a' and app.gameOver == False:
        app.autoModeOn = not app.autoModeOn
    elif key == 'd':
        app.xWingModeOn = not app.xWingModeOn

def play_onMousePress(app, mouseX, mouseY):
    currentCell = play_getCurrentCell(app, mouseX, mouseY)
    if intersectingRect(app.backButtonLeft, app.backButtonTop, 
                        app.backButtonWidth, app.backButtonHeight,
                        mouseX, mouseY):
        setActiveScreen('help')
    elif currentCell != None and app.gameOver == False:
        row, col = currentCell
        cellContent = app.board[row][col]
        if cellContent <= 0:
            app.selected = currentCell
            app.isHardSelected = True
            app.selectedRegions = set()
            #Updates the cells in the same region as the hardselected cell
            #For UI purposes
            for region in app.regions:
                if app.selected in region:
                    app.selectedRegions = app.selectedRegions | set(region)
            app.selectedRegions.remove(currentCell)
    else:
        app.selected = None
        app.isHardSelected = False
        app.selectedRegions = set()

def play_onMouseMove(app, mouseX, mouseY):
    currentCell = play_getCurrentCell(app, mouseX, mouseY)
    if app.isHardSelected == False and app.gameOver == False: 
        if currentCell != None:
            row, col = currentCell
            cellContent = app.board[row][col]
            if cellContent <= 0:
                app.selected = currentCell
        else:
            app.selected = None

def play_getCurrentCell(app, mouseX, mouseY):
    for row in range(app.rows):
        for col in range(app.cols):
            cellLeft, cellTop = getCellLeftTop(app, row, col)
            cellWidth, cellHeight = getCellSize(app)
            cellRight, cellBot = cellLeft + cellWidth, cellTop + cellHeight
            if ((cellLeft <= mouseX <= cellRight) and 
                (cellTop <= mouseY <= cellBot)):
                return (row, col)
    return None

def play_onStep(app):
    if not app.gameOver:
        app.steps += 1
        if app.autoModeOn and not isBoardWrong(app):
            changeHintedCell(app)
            setLegals(app)

#All draw code is down here.
#Color Scheme Guide from:
#https://www.oberlo.com/blog/color-combinations-cheat-sheet
#UI inspiration taken from NYT Sudoku:
#https://www.nytimes.com/puzzles/sudoku/easy 
#and Sudoku.com:
#https://sudoku.com
#Color taken from CS Academy:
#https://cs3-112-f22.academy.cs.cmu.edu/docs
def play_redrawAll(app):
    drawRect(0, 0, app.width, app.height, 
             fill='lightGreen', border='brown', borderWidth=3)
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
             fill='white')
    drawBoard(app)
    drawBackButton(app)
    draw3x3Blocks(app)
    drawBoardBorder(app)
    drawAutoModeIndicator(app)
    if isBoardWrong(app):
        drawWarningMessage(app)
    if app.gameOver:
        drawGameOver(app)
    drawClock(app)

def drawWarningMessage(app):
    cx, cy = 90, 300
    drawLabel('Wrong Values Exist', cx, cy, 
              fill='crimson', size=15, bold=True)
    drawLabel('Please Fix Them', cx, cy + 20, 
              fill='crimson', size=15, bold=True)
    drawLabel('No Hints', cx, cy + 40, 
              fill='crimson', size=15, bold=True)

def drawClock(app):
    seconds = (app.steps // 10)  % 60
    minutes = (app.steps // 10) // 60
    cx, cy = 90, 225

    drawRect(cx, cy, 100, 50, 
             fill='mintCream', border='black', align='center')
    if minutes < 10:
        drawLabel(f'0{minutes}', cx - 20, cy, size=25, bold=True)
    else:
        drawLabel(minutes, cx - 20, cy, size=25, bold=True)
    drawLabel(':', cx, cy,            size=25, bold=True)
    if seconds < 10:
        drawLabel(f'0{seconds}', cx + 20, cy, size=25, bold=True)
    else:
        drawLabel(seconds, cx + 20, cy,   size=25, bold=True)

def drawAutoModeIndicator(app):
    if app.autoModeOn:
        color = 'honeydew'
        label = 'ON' 
    else:
        color = 'mistyRose'
        label = 'OFF'
    cx, cy = 90, 100
    drawCircle(cx, cy, 50, fill=color, border='black')
    drawLabel('AUTO', cx, cy - 15, size=25, bold=True)
    drawLabel(label, cx, cy + 15, size=25, bold=True)

def drawGameOver(app):
    cx, cy = app.width/2, 290
    drawRect(cx, cy, 600, 200, 
             fill='gold', border='black', align='center')
    drawLabel('YOU WIN', cx, cy, bold=True, size=40)

def drawBackButton(app):
    cx = app.backButtonLeft + app.backButtonWidth/2
    cy = app.backButtonTop + app.backButtonHeight/2
    drawRect(cx, cy, 200, 100, fill='red', border='black', align='center')
    drawLabel('Back', cx, cy, size=60, bold=True)

def draw3x3Blocks(app):
    #Draws the boxes labeling 3x3 blocks 
    for row in range(app.rows):
        for col in range(app.cols):
            cellLeft, cellTop = getCellLeftTop(app, row, col)
            cellWidth, cellHeight = getCellSize(app)
            if row % 3 == 0 and col % 3 == 0: 
                drawRect(cellLeft, cellTop, cellWidth * 3, cellHeight * 3,
                        fill=None, borderWidth=2, border='red')

#Structure of draw code taken from 5.3.7 Creative Task (Tetris)
#https://cs3-112-f22.academy.cs.cmu.edu/exercise/4969
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)

def drawCell(app, row, col):
    #Draws the cell box
    if (row, col) == app.selected:
        color = 'pink' if app.isHardSelected else 'lightGray'
    elif (row, col) in app.hintedCells:
        color = 'yellow'
    elif (row, col) in app.selectedRegions:
        color = 'lavender'   
    else:
        color = None
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight, 
             fill=color, border='black', borderWidth=app.cellBorderWidth)
    #Draws the stuff inside each cell
    cx = cellLeft + cellWidth/2
    cy = cellTop  + cellHeight/2
    cellContent = app.board[row][col]
    labelColor = 'blue' if app.board[row][col] > 0 else 'black'
    if cellContent == 0:
        label = ''
    else:
        #Always displays positive numbers despite some board values
        #being stored as negatives
        label = str(abs((cellContent))) 
        #draw the red circle for wrong cells
        if abs(cellContent) != app.solutionBoard[row][col]:
            redX = cx + cellWidth  * 0.3
            redY = cy + cellHeight * 0.3
            drawCircle(redX, redY, 5, fill='red')
    drawLabel(label, cx, cy, size=30, fill=labelColor)

    #draw the legals for that cell
    if cellContent == 0 and app.legalModeOn:
        drawCellLegals(app, row, col)

def drawCellLegals(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    currentCellLegals = app.legalsBoard[row][col]
    for legal in currentCellLegals:
        i = (legal - 1) %  3
        j = (legal - 1) // 3
        cx = 12.5 + cellLeft + (cellWidth*0.8/3)  * i
        cy = 12.5 + cellTop  + (cellHeight*0.8/3) * j
        label = str(legal)
        drawLabel(label, cx, cy, fill='gray')

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def drawBoardBorder(app):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
             fill=None, border='black', borderWidth=(app.cellBorderWidth * 2))

######################
#Runs the App
######################
def main():
    runAppWithScreens(initialScreen='initial', width=800, height=800)

main()