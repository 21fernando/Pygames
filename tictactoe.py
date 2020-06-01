#This program is a basic tic tac toe game with a simple AI
#12/2/18
__author__='Tharindu Fernando'

import random
import copy
import time
player = '' #MINIMIZING
computer = ''#MAXIMIZING
firstCall = True
firstDepth = 0

#printBoard handles the Ascii art for the board and is given the board as a parameter
def printBoard(board):
  print('* Game Board *')
  for row in range(0, len(board)):
    for col in range (0, len(board[row])):
      print(' '+board[row][col], end=' ')
      if col == 0 or col == 1:
        print('|', end = '')
      else:
        print()
    if row==0 or row == 1:
      print("-----------")
    else:
      print('\n')

#isOpen checks if a certian square on the grid is open
def isOpen(board, r,c):
  return board[r][c] == ' '

#gameWon checks if the game has been won
def gameWon(board):
  i=0
  #All horizontal and vertical rows
  while i<=2:
    if (board[i][0] in 'XO') and board[i][0]!='' and board[i][0] == board[i][1] and board[i][1]== board[i][2]:
      return board[i][0]
    elif (board[0][i] in 'XO')and board[0][i]!='' and board[0][i] == board[1][i] and board[1][i]== board[2][i]:
      return  board[0][i]
    i+=1
  #top left to botom right
  if (board[0][0] in 'XO')and board[0][0]!='' and board[0][0] == board[1][1] and board[1][1]== board[2][2]:
    return  board[0][0]
  #top right to bottom left
  if (board[0][2]  in 'XO') and board[0][2]!=''and board[0][2] == board[1][1] and board[1][1]== board[2][0]:
    return  board[0][2]
  else: return False

#Checks if the board is full
def boardIsFull(board):
  if ' ' in board[0] or ' ' in board[1] or ' ' in board[2]:
    return False
  else:
    return True

#https://www.youtube.com/watch?v=l-hh51ncgDI
def miniMax (inputBoard, depth,alpha, beta, turn):
  global computer
  global player
  global firstCall
  global firstDepth
  if depth>firstDepth:
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
    for row in range(0,3):
      for col in range(0,3):
        boardCopy = copy.deepcopy(inputBoard) #https://stackoverflow.com/questions/6532881/how-to-make-a-copy-of-a-2d-array-in-python
        if not isOpen(boardCopy,row,col): continue
        boardCopy[row][col] = turn
        result = miniMax(boardCopy, depth-1,alpha,beta, computer)
        minScore = min(result, minScore)
        if result<minScore:
          minScore = result
          minMove[0]=row
          minMove[1]=col
        beta=min(beta, minScore)
        if beta<= alpha:
          break
    if depth == firstDepth:
      firstDepth = 0
      return minMove
    else:
      return minScore
  if turn == computer:
    maxScore = -10
    maxMove = [0,0]
    for row in range(0,3):
      for col in range(0,3):
        boardCopy = copy.deepcopy(inputBoard) #https://stackoverflow.com/questions/6532881/how-to-make-a-copy-of-a-2d-array-in-python
        if not isOpen(boardCopy,row,col): continue
        boardCopy[row][col] = turn
        result =miniMax(boardCopy, depth-1,alpha,beta, player)
        if result>maxScore:
          maxScore = result
          maxMove[0]=row
          maxMove[1]=col
        alpha = max(alpha, maxScore)
        if beta<=alpha:
          break
    if depth == firstDepth:
      firstDepth = 0
      return maxMove
    else:
      return maxScore

def computerMove(inputBoard, depth, player):
  move = miniMax(inputBoard, depth,-100,100, player)
  inputBoard[move[0]][move[1]] = player

#main method for the tic tac toe program
def main():
  global player
  global computer
  xTurn = random.randint(0,1) == 1
  print('* Welcome to Tic-Tac-Toe *')
  playing = True
  while playing:
    player = 'X'
    computer = 'O'
    xTurn = random.randint(0,1) == 1 #determine who plays 1st
    board = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
    while True:
      player = input("Would you like to be X or O?").upper()
      if player != 'X' and player != 'O':
        print('Invalid input')
      else:
        computer = 'O' if player == 'X' else 'X'
        break
    #Where the game is played
    while (not gameWon(board) == computer) and (not gameWon(board)==player) and (not boardIsFull(board)):
      printBoard(board)
       ###Handle xTurn
      if (player == 'X' and xTurn) or (player == 'O' and not xTurn):
        #Get and validate user input
        while True:
          try:
            moves = input('Select a row col to move, separating the values with a space (ex: 0 2): ').split()
            #The user enters more than 2 numbers
            if len(moves)>2:
              print('Please Enter Valid input')
              continue
            #If the user enters two zeroes
            if len(moves[0])>1 or len(moves[1])>1:
              print('Please Enter Valid input')
              continue
            moves = [int(moves[0]), int(moves[1])]
            #Can the user move to this spot
            if not isOpen(board, moves[0], moves[1]):
              print('That square is taken!')
              continue
            #Everything is valid if it gets here
            board[int(moves[0])][int(moves[1])] = player
            print('User moves to', moves)
            break
          #The user entered text or one number or some other kind of input error
          except:
            print('Please Enter Valid input')
      else:
        print('Computers turn...This first one may take a while')
        spaces = 0
        for row in range(0,3):
          for col in range(0,3):
            if isOpen(board,row,col):
              spaces+=1
        computerMove(board,spaces, computer)
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
      if again.lower()== 'no':
        playing = False
        break
      elif again.lower() == 'yes':
        break
      else:
        print('Invalid Input!')
  print('Thank you for playing!')
#main entry point
if __name__ == '__main__':
  main()