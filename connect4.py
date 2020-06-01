__author__ = 'Tharindu Fernando'

import random
import copy
import time

player = ''  # MINIMIZING
computer = ''  # MAXIMIZING
firstCall = True
firstDepth = 0


# printBoard handles the Ascii art for the board and is given the board as a parameter
def printBoard(board):
    print('* Game Board *')
    for row in range(0, len(board)):
        print("-----------------------------")
        for col in range(0, len(board[row])):
            print('| ' + board[row][col], end=' ')
            if col == len(board[0]) - 1:
                print('|')
        if row == len(board) - 1:
            print("-----------------------------")


# isOpen checks if a certain column is open
def isOpen(board, c):
    return board[0][c] == ' '


# Returns the lowest index in a column
def getLowest(board, c):
    i = 5
    while board[i][c] == " ":
        i -= 1;
    return 1


# gameWon checks if the game has been won
def gameWon(board):
    # horizontal rows
    for row in range(len(board)):
        for col in range(0, 4):
            if board[row][col] != ' ' and board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3]:
                return board[row][col]
    # Vertical rows
    for col in range(len(board[1])):
        for row in range(0, 3):
            if board[row][col] != ' ' and board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col]:
                return board[row][col]
    # Decreasing Diagonal
    for row in range(0, 3):
        for col in range(0, 4):
            if board[row][col] != ' ' and board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3]:
                return board[row][col]
    # Increasing Diagonal
    for row in range(3, 6):
        for col in range(3,7):
            if board[row][col] != ' ' and board[row][col] == board[row - 1][col - 1] == board[row - 2][col - 2] == board[row - 3][col - 3]:
                return board[row][col]
    return False


# Checks if the board is full
def boardIsFull(board):
    return ' ' not in board[0]


# https://www.youtube.com/watch?v=l-hh51ncgDI
def miniMax(inputBoard, depth, alpha, beta, turn):
    global computer
    global player
    global firstCall
    global firstDepth
    if depth > firstDepth:
        firstDepth = depth
    if gameWon(inputBoard) != False or boardIsFull(inputBoard):
        if gameWon(inputBoard) == computer:
            return 10 + depth
        elif gameWon(inputBoard) == player:
            return -10 - depth
        else:
            return 0
    if turn == player:
        minScore = 10
        minMove = []
        for row in range(0, 3):
            for col in range(0, 3):
                boardCopy = copy.deepcopy(
                    inputBoard)  # https://stackoverflow.com/questions/6532881/how-to-make-a-copy-of-a-2d-array-in-python
                if not isOpen(boardCopy, row, col): continue
                boardCopy[row][col] = turn
                result = miniMax(boardCopy, depth - 1, alpha, beta, computer)
                minScore = min(result, minScore)
                if result < minScore:
                    minScore = result
                    minMove[0] = row
                    minMove[1] = col
                beta = min(beta, minScore)
                if beta <= alpha:
                    break
        if depth == firstDepth:
            firstDepth = 0
            return minMove
        else:
            return minScore
    if turn == computer:
        maxScore = -10
        maxMove = [0, 0]
        for row in range(0, 3):
            for col in range(0, 3):
                boardCopy = copy.deepcopy(
                    inputBoard)  # https://stackoverflow.com/questions/6532881/how-to-make-a-copy-of-a-2d-array-in-python
                if not isOpen(boardCopy, row, col): continue
                boardCopy[row][col] = turn
                result = miniMax(boardCopy, depth - 1, alpha, beta, player)
                if result > maxScore:
                    maxScore = result
                    maxMove[0] = row
                    maxMove[1] = col
                alpha = max(alpha, maxScore)
                if beta <= alpha:
                    break
        if depth == firstDepth:
            firstDepth = 0
            return maxMove
        else:
            return maxScore


def computerMove(inputBoard, depth, player):
    move = miniMax(inputBoard, depth, -100, 100, player)
    inputBoard[move[0]][move[1]] = player


def genBoard(numRows, numCols):
    fin = []
    for c in range(numCols):
        row = []
        for i in range(numRows):
            row.append(" ")
        fin.append(row)
    return (fin)


# main method for the tic tac toe program
def main():
    global player
    global computer
    xTurn = random.randint(0, 1) == 1
    print('* Welcome to Tic-Tac-Toe *')
    playing = True
    while playing:
        player = 'X'
        computer = 'O'
        xTurn = random.randint(0, 1) == 1  # determine who plays 1st
        board = genBoard(7, 6)
        printBoard(board)
        while True:
            player = input("Would you like to be X or O?").upper()
            if player != 'X' and player != 'O':
                print('Invalid input')
            else:
                computer = 'O' if player == 'X' else 'X'
                break
        # Where the game is played
        while (not gameWon(board) == computer) and (not gameWon(board) == player) and (not boardIsFull(board)):
            printBoard(board)
            ###Handle xTurn
            if (player == 'X' and xTurn) or (player == 'O' and not xTurn):
                # Get and validate user input
                while True:
                    try:
                        moves = input(
                            'Select a row col to move, separating the values with a space (ex: 0 2): ').split()
                        # The user enters more than 2 numbers
                        if len(moves) > 2:
                            print('Please Enter Valid input')
                            continue
                        # If the user enters two zeroes
                        if len(moves[0]) > 1 or len(moves[1]) > 1:
                            print('Please Enter Valid input')
                            continue
                        moves = [int(moves[0]), int(moves[1])]
                        # Can the user move to this spot
                        if not isOpen(board, moves[0], moves[1]):
                            print('That square is taken!')
                            continue
                        # Everything is valid if it gets here
                        board[int(moves[0])][int(moves[1])] = player
                        print('User moves to', moves)
                        break
                    # The user entered text or one number or some other kind of input error
                    except:
                        print('Please Enter Valid input')
            else:
                print('Computers turn...This first one may take a while')
                spaces = 0
                for row in range(0, 3):
                    for col in range(0, 3):
                        if isOpen(board, row, col):
                            spaces += 1
                computerMove(board, spaces, computer)
            xTurn = not xTurn
        printBoard(board)
        if gameWon(board) == computer:
            print("Computer won the game")
        elif gameWon(board) == player:
            print('You won the game')
        else:
            print('The game resulted in a tie')
        while True:
            again = input('Do you want to play again? Yes or no')
            if again.lower() == 'no':
                playing = False
                break
            elif again.lower() == 'yes':
                break
            else:
                print('Invalid Input!')
    print('Thank you for playing!')


# main entry point
if __name__ == '__main__':
    main()
