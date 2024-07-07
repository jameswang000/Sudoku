This project's name is Cactus Sudoku and allows the user to play Sudoku with boards varying in difficulty from easy to evil and use hints on those boards.

How to run:
Download the project zip file. Run the included Python file named 
"jameswa2_Sudoku_Term_Project" in VSCode or any other IDE. 

The following libraries are necessary: sys, os, random, copy, itertools, and cmu_graphics
The folder, "tp-starter-files", contains the Sudoku boards and all other assets required to run the app. The file path to access the "tp-starter-files" folder might need to be changed to reflect local conditions.

To install cmu_graphics, go to this link: https://academy.cs.cmu.edu/desktop and follow the instructions provided. Ultimately, you will have to put the graphics folder in the same folder as the Python file. When you run 
the Python file make sure that your working direction is the folder named "Sudoku" for the paths to work correctly.

Game Play:
1. The user can play Sudoku like normal. Begin by pressing the start button on the splash screen. Next the user will click a button correspond to a given board difficulty. This will take the user to a play screen with the following features.

2. Hovering over a cell will change its color and make it selected. Clicking inside a cell will hard select it, changing its color and highlighting all of the regions of the board that cell is a part of. 

3. Pressing a number on the keyboard while a cell is hard selected will change the hard selected cell's content to the pressed number. Pressing 0 on a hard selected cell will make it empty again. Incorrect values have a red circle displayed in the cell.

4. The possible values in each cell (legals) are by default, automatically displayed and updated based on the user's placement of numbers in cells (moves). The user can choose to turn off the legals display. 

5. Once the Sudoku is solved, a "You Win" is displayed and the user can click the back button to selected a new difficulty and receive a new board.

Hotkeys:
"a" to enable the automatic solver.
"s" to play a hint, in the order of "Obvious Single", "Obvious Tuple", "X Wing"
"h" to highlight cells involved in a hint, in the same order above.
"l" to toggle legal displays on or off.
"n" to start a new game at the current difficulty.
"d" to activate xWingHintMode which only plays xWingHints for demonstration purposes.