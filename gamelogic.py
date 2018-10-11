#Project 4 Eric Vu 57054956
NONE = ''
class Board:
    def __init__(self, board_col, board_row, turn) ->None:
        board = []
        for col in range(board_col):
            board.append([])
            for row in range(board_row):
                board[-1].append(NONE)
        self._game_state = board
        self._turn = turn
        self._col = board_col
        self._row = board_row
        
        
    def cell_value(self, col:int, row:int) -> str:
        '''Determines the value of a cell on the game board'''
        return self._game_state[col][row]
    
    def flip_cells(self, column:int, row:int) -> [[str]]:
        '''Flips a given cell on the board to the current turn'''
        self._game_state[column][row] = self._turn
        return self._game_state

    def switch_turn(self) -> str:
        '''Switches the current turn of the game board'''
        if self._turn == 'BLACK':
            self._turn = 'WHITE'
        else:
            self._turn = 'BLACK'       
        return self._turn
    
    def opponent_turn(self) -> str:
        
        if self._turn == 'BLACK':
            return 'WHITE'
        else:
            return 'BLACK'

    def count_white_score(self) -> int:
        score = []
        for i in range(len(self._game_state)):
            for j in range(len(self._game_state[0])):
                if self.cell_value(i, j) == 'WHITE':
                    score.append(self.cell_value(i, j))
        return len(score)

    def count_black_score(self) -> int:
        score = []
        for i in range(len(self._game_state)):
            for j in range(len(self._game_state[0])):
                if self.cell_value(i, j) == 'BLACK':
                    score.append(self.cell_value(i, j))
        return len(score)
    
class InvalidOthelloMove(Exception):
    pass

class NoValidMovesLeft(Exception):
    pass

class SpotAlreadyTaken(Exception):
    pass

def check_all_for_valid(board: Board, turn: str) -> bool:
    '''Checks the entire board to see if there is atleast one available'''
    for column in range(board._col):
        for row in range(board._row):
            if board.cell_value(column, row) == NONE:
                if len(_check_eight_directions(board, column, row, turn)) > 0:
                    return True
    return False

def run_player_move(board: Board, col: int, row: int, turn) -> Board:
    '''Runs the player's move'''
    _is_valid_move(board, col, row, turn)
    pieces_to_flip = _check_eight_directions(board, col, row, turn)
    pieces_to_flip.append((col, row))
    _flip_pieces(board, pieces_to_flip)
    
def opposite_turn(turn:str) -> Board:
    '''Returns the opposite turn of the given turn'''
    if turn == 'BLACK':
        return 'WHITE'
    else:
        return 'BLACK'
    
def place_middle_pieces(board:Board, player1: str, player2: str)-> Board:
    board._game_state[int(board._col/2 - 1)][int(board._row/2 - 1)] = player1
    board._game_state[int(board._col/2)][int(board._row/2)] = player1
    board._game_state[int(board._col/2)][int(board._row/2 - 1)] = player2
    board._game_state[int(board._col/2 - 1)][int(board._row/2)] = player2
    
def determine_winning_player_more(board:Board) -> None:
    '''Determines the winning player(the player with more tiles) once the game is over'''
    if board.count_white_score() > board.count_black_score():
        return 'White wins!'
    if board.count_white_score() < board.count_black_score():
        return 'Black wins!'
    if board.count_white_score() == board.count_black_score():
        return 'Tie Game!'

def determine_winning_player_less(board: Board) -> None:
    '''Determines the winning player(the player with fewer tiles) once the game is over'''
    if board.count_white_score() < board.count_black_score():
        return 'White wins!'
    if board.count_white_score() > board.count_black_score():
        return 'Black wins!'
    if board.count_white_score() == board.count_black_score():
        return 'Tie Game!'


def _is_valid_move(board: Board, col: int, row: int, turn) -> None:
    '''Determines if a given move is valid'''
    _is_off_board(board, col, row)
    _is_empty_spot(board, col, row)
    _is_valid_atleast_one_direction(board, col, row, turn)

def _is_empty_spot(board:Board, col: int, row: int) -> None:
    '''Determines if a given cell is empty'''
    start_cell = board.cell_value(col, row)
    if start_cell != NONE:
        raise SpotAlreadyTaken()
    
def _is_off_board(board: Board, col:int, row:int) -> None:
    '''Determines if a given cell is off of the board'''
    if not 0<=col<=board._col or not 0<=row<=board._row:
        raise InvalidOthelloMove()
    
def _check_if_off_board(board:Board, col:int, row:int) -> bool:
    '''Checks to see if a given cell is off of the board and returns a boolean'''
    if not 0<=col<board._col or not 0<=row<board._row:
        return False
    return True

def _is_valid_atleast_one_direction(board: Board, col: int, row: int, turn) -> None:
    '''Checks to see if a a given cell is a valid move for the current turn'''
    if len(_check_eight_directions(board, col, row, turn)) == 0:
        raise InvalidOthelloMove()

def _check_eight_directions(board:Board, col: int, row: int, turn) -> list:
    '''Check's in all eight directions of a given move and returns
    a list of all coordinates to flip'''
    possible_directions = [-1, 0, 1]
    master_coordinate_list = []
    for i in possible_directions:
        for j in possible_directions:
            if  i != 0 or j != 0:
                master_coordinate_list.extend(_check_to_flip(board, col, row, i, j, turn))
    return master_coordinate_list

def _check_to_flip(board:Board, col: int, row: int, coldelta: int, rowdelta: int, turn:str) -> list:
    '''Checks in one direction to see if any pieces should be flipped, given a move'''
    
    col_row_list = []
    while True:
        if _check_if_off_board(board, col + coldelta, row + rowdelta):
            if board.cell_value(col+coldelta, row+rowdelta) == opposite_turn(turn):
                col_row_list.append((col+coldelta, row+rowdelta))
                col = col + coldelta
                row = row + rowdelta

            elif board.cell_value(col+coldelta, row+rowdelta) == turn:
                return col_row_list
                
            elif board.cell_value(col+coldelta, row+rowdelta) == NONE:
                col_row_list = []
                return col_row_list
        else:
            col_row_list = []
            return col_row_list
                               
def _flip_pieces(board: Board, coordinates: list) -> Board:
    '''
    Takes a list of coordinates and flips each piece in the list
    '''
    for coordinate in coordinates:
        board.flip_cells(coordinate[0], coordinate[1])
    
a = Board(8,8, 'BLACK')
