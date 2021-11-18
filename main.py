import numpy as np
import curses
from curses import wrapper
def main(stdscr):
    boardCoords = (6, 50) 
    playerTurn = True
    gameOver = False
    gameBoard = ResetBoard()
    ResetGame(stdscr, gameBoard, boardCoords)

    # gameloop
    while True:
        gameOver = CheckIfPlayerWon(stdscr, gameBoard)

        input = stdscr.getch()
        if input == ord('r'):
            gameBoard = ResetBoard()
            ResetGame(stdscr, gameBoard, boardCoords)
            playerTurn = True
            gameOver = False
        if input == 27:
            break
        if gameOver:
            continue
        playerTurn = HandlePlayerMove(stdscr, playerTurn, gameBoard, boardCoords, input)
        HandleCursorMovement(stdscr, input, boardCoords)



# Handles a player entering a move.
def HandlePlayerMove(stdscr, playerTurn, gameBoard, boardCoords, input):
    #Enter is not pressed or an illegal move is made
    (y, x) = stdscr.getyx()
    if input != curses.KEY_ENTER and input != 10 and input != 13: #ascii options for enter
        return playerTurn
    if gameBoard[(y - boardCoords[0]) / 2][(x - boardCoords[1]) / 2] == 'O' or gameBoard[(y - boardCoords[0]) / 2][(x - boardCoords[1]) / 2] == 'X':
        return playerTurn

    # A legal move is made so the player turn is switched and the board is altered
    input = 'X' if playerTurn else 'O'
    stdscr.addstr(y, x, input)
    if playerTurn:
        stdscr.addstr(boardCoords[0]+8, boardCoords[1]-5, "Player 2's Turn")
    else:
        stdscr.addstr(boardCoords[0]+8, boardCoords[1]-5, "Player 1's Turn")
    stdscr.move(y, x)
    gameBoard[(y - boardCoords[0]) / 2][(x - boardCoords[1]) / 2] = input
    return not playerTurn #flipping the current player


# Checks for player input to move the cursor. Does this in steps of two because of the extra borders of the ASCII art
def HandleCursorMovement(stdscr, input, boardCoords):
    (y, x) = stdscr.getyx()
    if input == ord('d') and x < boardCoords[1] + 4:
        stdscr.move(y, x+2)
    elif input == ord('a') and x > boardCoords[1]:
        stdscr.move(y, x-2)
    elif input == ord('w') and y > boardCoords[0]:
        stdscr.move(y-2, x)        
    elif input == ord('s') and y < boardCoords[0] + 4:
        stdscr.move(y+2, x)

# Uses the board matrix to check if any row, column or diagonal is filled with the an X or O, then return True if a player has won
def CheckIfPlayerWon(stdscr, gameBoard):
    diagonal = np.diag(gameBoard)
    reverseDiagonal = np.diag(np.fliplr(gameBoard))
    if np.any(np.all(gameBoard =='X', axis=1) == True) | np.any(np.all(gameBoard =='X', axis=0) == True) | np.all(diagonal == 'X') | np.all(reverseDiagonal == 'X'):  
        stdscr.addstr(15, 5, 'X is the winner!')
        stdscr.addstr(20, 5, 'To play again press R or press ESC to quit')
        return True   
    if np.any(np.all(gameBoard =='O', axis=1) == True) | np.any(np.all(gameBoard =='O', axis=0) == True) | np.all(diagonal == 'O') | np.all(reverseDiagonal == 'O'):  
        stdscr.addstr(15, 5, 'O is the winner!')
        stdscr.addstr(20, 5, 'To play again press R or press ESC to quit')
        return True
    return False

def ResetBoard():
    board = np.array([[' ', ' ', ' '], 
    [' ', ' ', ' '],
    [' ', ' ', ' ']])
    return board

def DrawBoard(stdscr, board, boardCoords):
    stdscr.addstr(1, 20, "Welcome to Tic-Tac-Toe! You can move the cursor with the WASD-keys.")
    stdscr.addstr(2, 20, "Press the Enter-key to make a move on the board. X goes first.")
    stdscr.addstr(3, 20, "Exit the game by pressing the Esc-key or reset with the R-key. Have fun!")
    stdscr.addstr(boardCoords[0], boardCoords[1], board[0][0] + '|' + board[0][1] + '|' + board[0][2])
    stdscr.addstr(boardCoords[0]+1, boardCoords[1], '-+-+-')
    stdscr.addstr(boardCoords[0]+2, boardCoords[1], board[1][0] + '|' + board[1][1] + '|' + board[1][2])
    stdscr.addstr(boardCoords[0]+3, boardCoords[1], '-+-+-')
    stdscr.addstr(boardCoords[0]+4, boardCoords[1], board[2][0] + '|' + board[2][1] + '|' + board[2][2])
    stdscr.refresh()

def ResetGame(stdscr, board, boardCoords):
    stdscr.erase()
    DrawBoard(stdscr, board, boardCoords)
    stdscr.addstr(boardCoords[0]+8, boardCoords[1]-5, "Player 1's Turn")
    stdscr.move(boardCoords[0], boardCoords[1])

wrapper(main)