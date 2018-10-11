#Project 4 Eric Vu 57054956
import gamelogic
def ask_for_column_numbers() -> int:
    '''Ask for even number of columns for the game board'''
    while True:
        column_num = int(input('Enter an even number specifying the amount of board columns:'))
        if column_num%2 == 0 and 4<=column_num<=16:
            return column_num
        else:
            print('Invalid input, please try again.')

def ask_for_row_numbers() -> int:
    '''Ask for even number of rows for the game board'''
    while True:
        row_num = int(input('Enter an even number specifying the amount of board rows:'))
        if row_num%2 == 0 and 4<=row_num<=16:
            return row_num
        else:
            print('Invalid input, please try again.')

def ask_for_starting_turn() -> str:
    '''Ask user to ask which turn to start'''
    while True:
        starting_turn = input('Which color starts? Black or White?').upper()
        if starting_turn == 'WHITE' or starting_turn == 'BLACK':
            return starting_turn
        else:
            print('Invalid input, please try again')

def determine_top_left_piece() -> str:
    '''Ask user to specify which piece is in the top left corner of the four
    pieces in the middle''' 
    while True:
        top_left_piece = input('Which piece will be on the top left? Black or White?').upper()
        if top_left_piece == 'WHITE' or top_left_piece == 'BLACK':
            return top_left_piece
        else:
            print('Invalid input, please try again.')

def determine_game_mode() -> str:
    while True:
        mode = input('Will the player with more points or less points win? Enter MORE or LESS').upper()
        if mode != 'MORE' and mode != 'LESS':
            print('Invalid input, please try again')
        else:
            return mode
        
def display(board: gamelogic.Board) -> None:
    '''
    Displays the current game state of the board in a readable format
    '''
    num_column = ''
    num_row = 0
    for column in range(board._col):
        num_column += str(column + 1) + ' '
    print('  ' + num_column)
    for row in range(board._row):
        num_row += 1
        print(str(num_row), end = ' ')
        for column in range(board._col):
            if board.cell_value(column, row) == 'BLACK':
                pixel = 'B'
            elif board.cell_value(column, row) == 'WHITE':
                pixel ='W'
            else:
                pixel = '.'

            print(pixel, sep='', end=' ')
        print()
    return

def place_middle_pieces(board:gamelogic.Board, player1: str, player2: str)-> gamelogic.Board:
    board._game_state[int(board._col/2 - 1)][int(board._row/2 - 1)] = player1
    board._game_state[int(board._col/2)][int(board._row/2)] = player1
    board._game_state[int(board._col/2)][int(board._row/2 - 1)] = player2
    board._game_state[int(board._col/2 - 1)][int(board._row/2)] = player2   

def user_interface() -> None:
    '''
    Runs user interface
    '''
    board_columns = ask_for_column_numbers()
    board_rows = ask_for_row_numbers()
    turn = ask_for_starting_turn()
    board = gamelogic.Board(board_columns, board_rows, turn)
    top_left_piece = determine_top_left_piece()
    top_right_piece = gamelogic.opposite_turn(top_left_piece)
    gamelogic.place_middle_pieces(board, top_left_piece, top_right_piece)
    game_mode = determine_game_mode()
    display(board)
    while True:
        opponent_turn = board.opponent_turn()
        print('White: ' + str(board.count_white_score()))
        print('Black: ' + str(board.count_black_score()))

        if gamelogic.check_all_for_valid(board, board._turn):
            print(board._turn + "'s turn")
            try:
                col_move = int(input('Which column?')) - 1
                row_move = int(input('Which row?')) - 1
                gamelogic.run_player_move(board, col_move, row_move, board._turn)
                board.switch_turn()

            except:
                print('Invalid Move, Please Try Again')

        else:
            print('No valid moves for ' + board._turn)
            if gamelogic.check_all_for_valid(board, opponent_turn) == False:
                print('No valid moves for ' + opponent_turn)
                if game_mode == 'MORE':
                    gamelogic.determine_winning_player_more(board)
                elif game_mode == 'LESS':
                    gamelogic.determine_winning_player_less(board)
                break
            else:
                board.switch_turn()
        display(board)
if __name__ == '__main__':
    user_interface()
