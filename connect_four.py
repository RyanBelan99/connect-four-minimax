#!/usr/bin/env python3
# Connect-Four with a minimax AI opponent.
# Author: Ryan Belan
# Course: CSC 242 (Introduction to AI), University of Rochester

import copy

#main board object class
class Board:
    def __init__(self,m,n):
        self.bd = zeros(m,n)
        self.m = m
        self.n = n 

#Fills 2darray with zeros
def zeros(m,n):
    o_list = []
    for row in range(m):
        i_list = []
        for col in range(n):
            i_list.append(0)
        o_list.append(i_list)
    return o_list        

#Cleanly prints board
def print_board(board):
    for row in board.bd:
        print(*row)
        

#Main method running the game. Operates on a while loop until a player reaches winning pattern 
def play(board):   
    bot_check = True
    game_status = True
    #Players turn
    while game_status:
        print("-----------------------")
        print_board(board)
        if bot_check:
            choice = int(input("Player make a move[1-...]: ")) - 1 
            if choice < board.n and check_col_full(board,choice):
                board.bd[check_opening(board,choice)][choice] = 1
                if check_if_win(board,1):
                    print_board(board)
                    game_status = False
                    print("You Won!!!") 
                bot_check = False    
            else:
                print("incorrect input! Try again!")
        #AI's turn        
        else:
            #choice = int(input("Bot make a move(1-...): ")) - 1 
            choices = []
            best_choice = None
            open_s = open_col(board)
            for x in range(len(open_s)):
                if(open_s[x] != -1):
                    temp = copy.deepcopy(board)
                    temp.bd[open_s[x]][x] = 2
                    depth = 0
                    choices.append(minimax(temp,False,depth+1))
                    if best_choice == None or choices[x] >= best_choice:
                        best_choice = choices[x]
                else: 
                    choices.append(None)    
            choice_index = choices.index(best_choice)
            if check_col_full(board,choice_index):
                board.bd[open_s[choice_index]][choice_index] = 2
                if check_if_win(board,2):
                    print_board(board)
                    game_status = False 
                    print("AI Won!!!")
                bot_check = True    
            else:
                print("incorrect input! Try again!")                  

def check_col_full(board,col):
    return board.bd[0][col] == 0
    
def check_opening(board,col):
    for x in range(board.m):
        if board.bd[board.m-x-1][col] == 0:
            return board.m-x-1

def create_env():
    print("Welcome to AI Connect-Four")
    print("1: 3x3 board  \n2: 6x7 board")
    select = int(input("Pick[1 or 2]: "))
    if select == 1:
        play(Board(3,3))
    elif select == 2:
        play(Board(6,7))
    else:
        print("invalid input!")  

#This method checks if a win pattern is on the board. This is called after each play on main board by either AI or Player. This is programmed for 3x3 and 6x7 board. 
def check_if_win(board, coin):
    diff = 3
    if board.m == 3:
        diff = 2
    #Call's each win pattern   
    return check_h(board,diff, coin) or check_v(board, diff, coin) or check_r_slope(board, diff, coin) or check_l_slope(board, diff, coin)

#Checks horizontal win pattern
def check_h(board, diff, coin):
    for col in range(board.n - diff):
        for row in range(board.m):
            if board.m == 6:
                if board.bd[row][col] == coin and board.bd[row][col+1] == coin and board.bd[row][col+2] == coin and board.bd[row][col+3] == coin:
                    return True
            else:
                if board.bd[row][col] == coin and board.bd[row][col+1] == coin and board.bd[row][col+2] == coin:
                    return True
    return False                

#Checks vertical win pattern 
def check_v(board, diff, coin):
    for col in range(board.n):
        for row in range(board.m - diff):
            if board.m == 6:
                if board.bd[row][col] == coin and board.bd[row+1][col] == coin and board.bd[row+2][col] == coin and board.bd[row+3][col] == coin:
                    return True
            else:
                if board.bd[row][col] == coin and board.bd[row+1][col] == coin and board.bd[row+2][col] == coin:
                    return True
    return False 

#Checks for positive right slope wiin pattern 
def check_r_slope(board, diff, coin):
    for col in range(board.n - diff):
        for row in range(board.m - diff):
            if board.m == 6:
                if board.bd[row][col] == coin and board.bd[row+1][col+1] == coin and board.bd[row+2][col+2] == coin and board.bd[row+3][col+3] == coin:
                    return True
            else:
                if board.bd[row][col] == coin and board.bd[row+1][col+1] == coin and board.bd[row+2][col+2] == coin:
                    return True
    return False 

#Checks for negative left slope win pattern
def check_l_slope(board, diff, coin):
    for col in range(board.n - diff):
        # Start at `diff` so row-1..row-diff never go negative (which would
        # wrap around in Python and report a false diagonal win).
        for row in range(diff, board.m):
            if board.m == 6:
                if board.bd[row][col] == coin and board.bd[row-1][col+1] == coin and board.bd[row-2][col+2] == coin and board.bd[row-3][col+3] == coin:
                    return True
            else:
                if board.bd[row][col] == coin and board.bd[row-1][col+1] == coin and board.bd[row-2][col+2] == coin:
                    return True
    return False     

# AI Code
# Used a DFA to traverse a tree to each terminal state. Then the program uses minimax algorithm to determine best move.
# If prgram get to a certain depth(3) program makes an imperfect prediction on what state it's in. (predict method)
def minimax(temp_board, maximizing_position, depth):
    open_spots = open_col(temp_board)
    #This score the player min
    if check_if_win(temp_board, 1): 
        return -1
    #This scores the AI max    
    if check_if_win(temp_board, 2): 
        return 1
    #This scores a tie    
    if open_spots.count(-1) == temp_board.n:
        return 0
    #This is for 6x6 (part 2) making impefect decision for alpha and beta pruning    
    if depth == 5 and temp_board.m == 6:
        return predict(temp_board)
    #Max 
    if maximizing_position:
        max_eval = -1 
        for x in range(len(open_spots)):
            if(open_spots[x] != -1):
                temp = copy.deepcopy(temp_board)
                temp.bd[open_spots[x]][x] = 2
                eval = minimax(temp, False, depth+1)
                max_eval = max(max_eval,eval)                    
        return max_eval
    #Min    
    else:
        min_eval = 1
        for x in range(len(open_spots)):
            if(open_spots[x] != -1):
                temp = copy.deepcopy(temp_board)
                temp.bd[open_spots[x]][x] = 1
                eval = minimax(temp, True, depth+1)
                min_eval = min(min_eval,eval)        
        return min_eval  

#This method is for part two which implements the heuristic depth into minimax
def predict(board):
    for col in range(board.n - 3):
        for row in range(board.m):
            if board.bd[row][col] == 2 and board.bd[row][col+1] == 2 and board.bd[row][col+2] == 2:
                return 1
            if board.bd[row][col] == 1 and board.bd[row][col+1] == 1 and board.bd[row][col+2] == 1:
                return -1
    for col in range(board.n - 3):
        # Start at row 2 so row-1/row-2 never wrap to a negative index.
        for row in range(2, board.m):
            if board.bd[row][col] == 2 and board.bd[row-1][col+1] == 2 and board.bd[row-2][col+2] == 2:
                return 1
            if board.bd[row][col] == 1 and board.bd[row-1][col+1] == 1 and board.bd[row-2][col+2] == 1:
                return -1
    for col in range(board.n - 3):
        for row in range(board.m - 3):
            if board.bd[row][col] == 2 and board.bd[row+1][col+1] == 2 and board.bd[row+2][col+2] == 2:
                return 1              
            if board.bd[row][col] == 1 and board.bd[row+1][col+1] == 1 and board.bd[row+2][col+2] == 1:
                return -1
    for col in range(board.n):
        for row in range(board.m - 3): 
            if board.bd[row][col] == 2 and board.bd[row+1][col] == 2 and board.bd[row+2][col] == 2:
                return 1  
            if board.bd[row][col] == 1 and board.bd[row+1][col] == 1 and board.bd[row+2][col] == 1:
                return -1
    return 0    

#This method fineds all of the available columns with will row index. If row is full it's marked -1 
def open_col(board):
    open = []
    for col in range(board.n):
        temp = check_opening(board,col)
        if temp == None:
            open.append(-1)
        else:
            open.append(temp)
    return open


if __name__ == '__main__':
    create_env()