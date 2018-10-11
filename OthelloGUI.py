# Eric Vu 57054956
import tkinter
import gamelogic
class Othello:
    def __init__(self):
        self._root_window = tkinter.Tk()
        self._game_title = self._root_window.title('Othello Game')
        self._menu_frame = tkinter.Frame(master = self._root_window, background = 'bisque', width = 500, height = 500) 
        self._menu_frame.grid(row = 0, column = 0, rowspan = 2, columnspan = 1,
                              sticky =  tkinter.W + tkinter.E)
        start_button = tkinter.Button(master = self._menu_frame, text = 'Start Game',
                                            command = self._delete_menu) # Button that exits menu page and starts game

        options_label = tkinter.Label(master = self._menu_frame, text = 'Game Options',
                                      font = ('Helvetica', 20))
        
        self._row_title = 'Choose Number of Rows'
        self._col_title = 'Choose Number of Columns'
        self._start_turn_title = 'Pick Who Goes First'
        self._top_left_title = 'Top Left Piece Color'
        self._game_title = 'Choose Game Option'

        self._var_row = tkinter.StringVar() #Used to get row numbers
        self._var_row.set(self._row_title)
        
        self._var_col = tkinter.StringVar() #Used to get column numbers
        self._var_col.set(self._col_title)
        
        self._starting_turn = tkinter.StringVar() #Used to get starting turn
        self._starting_turn.set(self._start_turn_title)
        
        self._top_left_piece = tkinter.StringVar() # Used to get top left piece
        self._top_left_piece.set(self._top_left_title)
        
        self._game_mode = tkinter.StringVar() # Used to get game mode
        self._game_mode.set(self._game_title)

        row_menu = tkinter.OptionMenu(self._menu_frame, self._var_row,
                                            '4', '6', '8', '10', '12', '14', '16')

        col_menu = tkinter.OptionMenu(self._menu_frame, self._var_col,
                                            '4', '6', '8', '10', '12', '14', '16')

        starting_turn_menu = tkinter.OptionMenu(self._menu_frame, self._starting_turn,
                                                      'BLACK', 'WHITE')
        top_left_piece_menu = tkinter.OptionMenu(self._menu_frame,
                                                       self._top_left_piece,
                                                       'BLACK', 'WHITE')
        game_mode_menu = tkinter.OptionMenu(self._menu_frame, self._game_mode,
                                                  'Player With More Pieces Wins', 'Player With Less Pieces Wins')
        options_label.grid(row = 0, column = 1, sticky = tkinter.N + tkinter.W + tkinter.E)
        row_menu.grid(row = 1, column = 1, sticky =  tkinter.W + tkinter.E,
                      padx = 10, pady = 10)
        col_menu.grid(row = 2, column = 1, sticky = tkinter.W + tkinter.E,
                      padx = 10, pady = 10)
        starting_turn_menu.grid(row = 3, column = 1, sticky = tkinter.W + tkinter.E,
                                padx = 10, pady = 10)
        top_left_piece_menu.grid(row = 4, column =1, sticky = tkinter.W + tkinter.E,
                                 padx = 10, pady = 10)
        game_mode_menu.grid(row = 5, column = 1, sticky = tkinter.W + tkinter.E,
                            padx = 10, pady = 10)
        start_button.grid(row = 6, column = 1, sticky = tkinter.W + tkinter.E,
                          padx = 10, pady = 10)
        
        self._root_window.rowconfigure(0, weight = 1)
        self._root_window.rowconfigure(1, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)
        for i in range(6):
            self._menu_frame.rowconfigure(i, weight = 1)
        self._menu_frame.columnconfigure(1, weight = 1)

    def _delete_menu(self) -> None:
        '''Deletes game options menu, and creates game board'''
        if self._var_row.get() != self._row_title and self._var_col.get() != self._col_title and self._starting_turn.get() != self._start_turn_title and self._top_left_piece.get() != self._top_left_title and self._game_mode.get() != self._game_title:
            ## Next few lines will set up board state
            self._row = int(self._var_row.get())
            self._column = int(self._var_col.get())
            top_right_piece = gamelogic.opposite_turn(self._top_left_piece.get())
            self._board = gamelogic.Board(self._column, self._row, self._starting_turn.get())
            gamelogic.place_middle_pieces(self._board, self._top_left_piece.get(), top_right_piece)
            
            ## Destroys the menu page and creates game board
            self._menu_frame.destroy()

            ## Creates widgets for game board
            self._black_score = tkinter.Label(master = self._root_window, text = 'Black: ' + str(self._board.count_black_score()))
            self._white_score = tkinter.Label(master = self._root_window, text = 'White: ' + str(self._board.count_white_score()))
            self._white_score.grid(row = 0, column = 0, sticky = tkinter.N + tkinter.E)
            self._board_frame = tkinter.Frame(master = self._root_window, width = 500)

            self._current_turn = tkinter.Label(master = self._root_window, text = self._board._turn + "'s turn")
            self._current_turn.grid(row = 0, column = 0)
            
            self._canvas = tkinter.Canvas(master = self._board_frame, width = self._column*75, height = self._row*75,
                                background = "bisque", highlightthickness = 5)
            
            ## Places widgets on grid
            self._canvas.grid(row = 0, column = 0, rowspan = self._row, columnspan = self._column, 
                    sticky = tkinter.N + tkinter.S + tkinter.W + tkinter.E)
    
            self._board_frame.grid(row = 1, column = 0,
                                   sticky = tkinter.N + tkinter.S + tkinter.W + tkinter.E)
            self._black_score.grid(row = 0, column = 0,
                                   sticky = tkinter.N + tkinter.W)

            ## Binds canvas to events
            self._canvas.bind('<Button-1>', self._on_canvas_clicked)
            self._canvas.bind('<Configure>', self._on_canvas_resized)
    
            self._root_window.rowconfigure(0, weight =0)
            self._root_window.rowconfigure(1, weight = 1)
            self._root_window.columnconfigure(0, weight = 1)
            
            for i in range(self._row):
                self._board_frame.rowconfigure(i, weight = 1)
            for j in range(self._column):
                self._board_frame.columnconfigure(j, weight = 1)

        else:
            pass

    def start(self) -> None:
        '''Mainloops the root window'''
        self._root_window.mainloop()

    def _on_canvas_resized(self, event: tkinter.Event) -> None:
        '''Redraws game board according to the new size of the window'''
        self._redraw_game_board()

    def _redraw_game_board(self) -> None:
        '''Deletes game board and redraws it to fit the new size of the window'''
        self._delete_board()

        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()
        
        self._draw_score()
        self._draw_pieces(canvas_width, canvas_height)        
        self._draw_grid(canvas_width, canvas_height)

    def _delete_board(self) -> None:
        '''Deletes current game board display'''
        self._black_score.destroy()
        self._white_score.destroy()
        self._current_turn.destroy()
        self._canvas.delete(tkinter.ALL)

    def _draw_score(self) -> None:
        '''Displays the current score of each player as well as whose turn it is'''
        self._black_score = tkinter.Label(master = self._root_window,
                                          text = 'Black: ' + str(self._board.count_black_score()))
        self._black_score.grid(row = 0, column = 0, sticky = tkinter.N + tkinter.W)
        self._white_score = tkinter.Label(master = self._root_window,
                                          text = 'White: ' + str(self._board.count_white_score()))
        self._white_score.grid(row = 0, column = 0, sticky = tkinter.N + tkinter.E)
        self._current_turn = tkinter.Label(master = self._root_window, text = self._board._turn + "'s turn")
        self._current_turn.grid(row = 0, column = 0)

    def _draw_grid(self, width, height) -> None:
        '''Draws the boxes of the game board'''
        for i in range(self._row):
           for j in range(self._column):
               x1 = (width/self._column)*j
               x2 = x1 + width/self._column
               y1 = (height/self._row)*i
               y2 = y1 + height/self._row
               self._canvas.create_rectangle(x1, y1, x2, y2, width = 1.5)
                
    def _draw_pieces(self, width, height) -> None:
        '''Draws all of the pieces currently on the Board'''
        for i in range(len(self._board._game_state)):
            for j in range(len(self._board._game_state[0])):
                if self._board._game_state[i][j] == 'WHITE':
                    self._draw_piece(i, j, 'WHITE', width, height)
                elif self._board._game_state[i][j] == 'BLACK':
                    self._draw_piece(i, j, 'BLACK', width, height)
                
    def _draw_piece(self, col: int, row: int, color: str, width: float, height: float) -> None:
        '''Given a cell, draws a game piece in that cell'''
        shrink_size = (width/self._column)/20
        x1 = width/self._column * col
        x2 = x1 + width/self._column
        y1 = height/self._row * row
        y2 = y1 + height/self._row
        self._canvas.create_oval(x1+shrink_size, y1+shrink_size, x2 - shrink_size, y2 - shrink_size,
                                 fill = color, outline = color)    
    
    def _on_canvas_clicked(self, event: tkinter.Event) -> None:
        '''Runs the player move depending on where the player clicked'''
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
        grid_coordinate = self._board_frame.grid_location(event.x, event.y)
        try:
            gamelogic.run_player_move(self._board, grid_coordinate[0], grid_coordinate[1], self._board._turn)
            self._board.switch_turn()
            self._redraw_game_board()

            if self._check_for_valid_move(self._board._turn) == False:
                if self._check_for_valid_move(self._board.opponent_turn()) == False:
                    self._current_turn.destroy()
                    if self._game_mode.get() == 'Player With More Pieces Wins':
                        self._winning_player = tkinter.Label(master = self._root_window,
                                                              text = gamelogic.determine_winning_player_more(self._board))
                        self._winning_player.grid(row = 0, column = 0)
                    elif self._game_mode.get() == 'Player With Less Pieces Wins':
                        self._winning_player = tkinter.Label(master = self._root_window,
                                                              text = gamelogic.determine_winning_player_less(self._board))
                        self._winning_player.grid(row = 0, column = 0)

                else:
                    self._board.switch_turn()
                    self._redraw_game_board()
        except:
            pass

    def _check_for_valid_move(self, turn: str):
        '''Determines if a valid move can be made for the inputted turn'''
        return gamelogic.check_all_for_valid(self._board, turn)

if __name__ == '__main__':
    Othello().start()
