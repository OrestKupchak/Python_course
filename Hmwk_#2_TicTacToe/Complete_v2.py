import random
import time

def choose_game_mode():
    game_mode = 0
    players = int(input("How many players will play? 0 or 1 or 2? Put an integer value: "))
    if players == 0:
        game_mode = 0
        print("Watch the clash of two AIs !")
    elif players == 1:
        game_mode = 1
        print("Prepare to fight the Artificial Intelligence !")
    elif players == 2:
        game_mode = 2
        print("Prepare to defeat your opponent ")
    else:
        print("That's a game for two!")
        game_mode = choose_game_mode()
    return game_mode

#---------------------------------------------------
#draw board/ set players/ apply player's choice to the board cells

correct_input = True
while correct_input == True:
        try:
            board_size = int(input("What row-column size of a board you would like to play? Put an integer value: "))
            fields_to_win = int(input("How many fields would be considered as victory? Put an integer value:  "))
        except ValueError:
            print ("Put an integer value!")
            continue
        else:
            correct_input = False
            break

#------------------------------------------------------------------------------
#prepare structures for rednering board/storing columns, rows, diagonals
vertical = '|     |'
horizontal = ' _____ ' 

board = [[' ' for x in range(board_size)] for y in range(board_size)] #grafical board 'X'/'O'
choices_board = [[0 for x in range(board_size)] for y in range(board_size)] #logical board 1/-1 to store players moves for win check
     #prepare structures for storing all posible columns, rows, diagonals of the board of defined size

max_col = len(choices_board[0]) 
max_row = len(choices_board)    
cols = [ list() for elements in range(max_col)] 
rows = [ list()  for elements in range(max_row)]
leftToRightDiagonal = [ list() for elements in range(max_row + max_col - 1)]
rightToLeftDiagonal = [ list() for elements in range(len(leftToRightDiagonal))]
min_diag = -max_row + 1

valid_verticals = []
valid_horizontals = []
valid_leftToRightDiagonal = []
valid_rightToLeftDiagonal = []

empty_fields = list()
cordinate = tuple()
for x in range(max_col):
    for y in range(max_row):  
        cordinate = (x,y)
        empty_fields.append(cordinate)

#------------------------------------------------------------
#draw graphical board of given size

def render_board(): 
    placeholder = ''  #invisible cells within each board field, where players previous move's choice will be showed
    x_axis = ''      #sequence of numbers for user's navigation of fileds on 'X' axis

    print('\n') #add margin between board and input 

    for i in range(len(board[0])):
        x_axis += str(i) + '      ' #add padding for alignment between axis flags 
    print('    ', x_axis)           #add margin for alignment of axis flags to board fields

    for i in range(len(board)):
        y_axis = i                          #sequence of numbers for users navigation of fileds on 'Y' axis
        for j in range(len(board[i])):
            placeholder += '|  '+ board[i][j] +'  |' #add placehoder for players input into field on visible board
        print('  ', horizontal*board_size)      #|
        print('  ', vertical*board_size)        #|add vertical and horizontal lines for fields 
        print(str(y_axis).rjust(2), placeholder)#|4,align y_axis to the right, for proper rendering if values are 2 or 3 digits
        placeholder = ''                        #|
    print('  ', horizontal*board_size)  
    print('\n') #add margin between board and input 


def cleanup_previous_check(choices_board):
    for x in range(max_col):
        for y in range(max_row):
            cols[x].pop()  if cols[x] else None
            rows[y].pop()  if rows[x] else None
        for y in range(max_row):    
            leftToRightDiagonal[x+y].pop() if leftToRightDiagonal[x+y] else None
            rightToLeftDiagonal[x-y-min_diag].pop() if rightToLeftDiagonal[x-y-min_diag] else None 

#---------------------------------------------------
#get columns, rows, diagonals from current board
def check_current_moves(choices_board):
        #populate respective structures with data from current board state
    cleanup_previous_check(choices_board)   
    for x in range(max_col):
        for y in range(max_row):
            cols[x].append(choices_board[y][x])
            rows[y].append(choices_board[y][x])
            leftToRightDiagonal[x+y].append(choices_board[y][x])
            rightToLeftDiagonal[x-y-min_diag].append(choices_board[y][x])

#------------------------------------------------------------
#switch players and make moves on board

#computer player to play in game_mode = 0 (PC vs.PC) and game_mode = 1 (player vs.PC)
def auto_playerMove(player, board):

        coord = random.choice(empty_fields) 
        x = coord[0]
        y = coord[1]

        if player == 1:
            board[x][y] = 'X'       #show choice on visual board
            choices_board[x][y] = 1 #add choice to logical board for win tracking
            empty_fields.pop(empty_fields.index((x,y)))
        if player == 2: 
            board[x][y] ='0'
            choices_board[x][y] = -1
            empty_fields.pop(empty_fields.index((x,y)))
        time.sleep(2)  
        print("Player {}, made his move on --> row_number, col_number: ".format(player), x, ',',y)    
        #return choices_board
        check_current_moves(choices_board)



def playerMove(player, board):

    correct_input = True
    while correct_input == True:
        try:
            x, y = input("Player {}, please enter coordinates for your move in format --> row_number, col_number: ".format(player)).split(',')
            x = int(x)
            y = int(y)

            if x > max_col-1:
                print ("Coordinate is out of the board!")
                playerMove(player, board)
            if y > max_row-1:
                print ("Coordinate is out of the board!")
                playerMove(player, board)
        except ValueError:
            print ("Invalid: Enter coordinates in correct format!")
            continue
        else:
            correct_input = False
            break

    print("X == ", x, "Y == ", y, board, "board[x][y] == ", board[x][y])
    if board[x][y] == ' ':
        # Check whether x, y is a valid choice, that is: not taken yet
        if player == 1:
            board[x][y] = 'X'       #show choice on visual board
            choices_board[x][y] = 1 #add choice to logical board for win tracking
        if player == 2: 
            board[x][y] ='0'
            choices_board[x][y] = -1
        #return choices_board
        check_current_moves(choices_board)
    else:
        print("You can move on empty fileds only!")
        playerMove(player, board)
    print("X == ", x, "Y == ", y, board, "board[x][y] == ", board[x][y])


 #---------------------------------------------------------      
 #check_current_moves(move), only posiible win combiantions of filed for definex 'size' and 'fields_to_win' values
def validate_moves(): 
    #check_current_moves(move)   #receive current state of board after each player's move

         #prepare structures for possible win combinations based on defined 'fields_to_win' value, may be variable 
    for valid in cols:
        if len(valid) >= fields_to_win :
            valid_verticals.append(valid)

    for valid in rows:
        if len(valid) >= fields_to_win :
            valid_horizontals.append(valid)

    for valid in leftToRightDiagonal:
        if len(valid) >= fields_to_win :
            valid_leftToRightDiagonal.append(valid)

    for valid in rightToLeftDiagonal:
        if len(valid) >= fields_to_win :
            valid_rightToLeftDiagonal.append(valid)

#---------------------------------------------------
#define_win_combinations_map

temp_res = list() #prepare structure to store interim results

def define_win_combinations_map(list):
    for comb in list:
        if len(comb) >= fields_to_win:

             for i, item in enumerate(comb):                      # valid win combinations should be chunks 
                if len(comb[i:i+fields_to_win]) == fields_to_win: # with length of defined 'fields_to_win'
                    temp_res.append(comb[i:i+fields_to_win]) 

def boards_status():
    define_win_combinations_map(valid_verticals)
    define_win_combinations_map(valid_horizontals)
    define_win_combinations_map(valid_leftToRightDiagonal)
    define_win_combinations_map(valid_rightToLeftDiagonal)


#------------------------------------------------------
#compare current board with winning combinations

def checkTotalTurns(fields_combination): 
    choice_results = 0
    for choice_map in fields_combination:
        for choice in choice_map:
            choice_results += choice
        if choice_results == fields_to_win:
            return "Winner is player 'X' !"               
        elif choice_results == -fields_to_win:
            return "Winner is player '0' !"             
        else:
            choice_results = 0
        #return "It's a draw !"  



#checkTotalTurns(temp_res)

#--------------------------------------
#play Game

def playGame():
    finished = False
    game_mode = choose_game_mode()
    player = random.randrange(1, 2, 1)  #define Player: 1 = 'X'/ 2 = 'O' randomly
    while not finished:
        render_board()                  # print board with current state after previous move
        if game_mode == 0:
            auto_playerMove(player, board)
        elif game_mode == 1:
            playerMove(player, board)  
            player = 3 - player
            auto_playerMove(player, board) 
        elif game_mode == 2:    
            playerMove(player, board)               # make another player move (set value to board on empty field)
        
        validate_moves()
        boards_status()
        win = checkTotalTurns(temp_res)
        if win:       # check for win/end, set finished accordingly
            render_board()
            print(win)
            finished = True         
        player = 3 - player             # switch players 1/2
        
playGame()