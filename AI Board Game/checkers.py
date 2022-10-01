from math import ceil
from functools import reduce
from copy import deepcopy

class Piece:

    def __init__(self):
        self.player = None
        self.other_player = None
        self.king = False
        self.captured = False
        self.position = None
        self.board = None
        self.capture_move_enemies = {}
        self.reset_for_new_board()

    def reset_for_new_board(self):
        self.possible_capture_moves = None
        self.possible_positional_moves = None

    def is_movable(self):
        return (self.get_possible_capture_moves()
                or self.get_possible_positional_moves()) \
            and not self.captured

    def capture(self):
        self.captured = True
        self.position = None

    def move(self, new_position):
        self.position = new_position
        self.king = self.king or self.is_on_enemy_home_row()

    def get_possible_capture_moves(self):
        if self.possible_capture_moves == None:
            self.possible_capture_moves = \
                self.build_possible_capture_moves()

        return self.possible_capture_moves

    def build_possible_capture_moves(self):
        adjacent_enemy_positions = list(filter(lambda position: \
                position \
                in self.board.searcher.get_positions_by_player(self.other_player),
                self.get_adjacent_positions()))
        capture_move_positions = []

        for enemy_position in adjacent_enemy_positions:
            enemy_piece = \
                self.board.searcher.get_piece_by_position(enemy_position)
            position_behind_enemy = \
                self.get_position_behind_enemy(enemy_piece)

            if position_behind_enemy != None \
                and self.board.position_is_open(position_behind_enemy):
                capture_move_positions.append(position_behind_enemy)
                self.capture_move_enemies[position_behind_enemy] = \
                    enemy_piece

        return self.create_moves_from_new_positions(capture_move_positions)

    def get_position_behind_enemy(self, enemy_piece):
        current_row = self.get_row()
        current_column = self.get_column()
        enemy_column = enemy_piece.get_column()
        enemy_row = enemy_piece.get_row()
        column_adjustment = (-1 if current_row % 2 == 0 else 1)
        column_behind_enemy = (current_column
                               + column_adjustment if current_column
                               == enemy_column else enemy_column)
        row_behind_enemy = enemy_row + enemy_row - current_row

        return self.board.position_layout.get(row_behind_enemy,
                {}).get(column_behind_enemy)

    def get_possible_positional_moves(self):
        if self.possible_positional_moves == None:
            self.possible_positional_moves = \
                self.build_possible_positional_moves()

        return self.possible_positional_moves

    def build_possible_positional_moves(self):
        new_positions = list(filter(lambda position: \
                             self.board.position_is_open(position),
                             self.get_adjacent_positions()))

        return self.create_moves_from_new_positions(new_positions)

    def create_moves_from_new_positions(self, new_positions):
        return [[self.position, new_position] for new_position in
                new_positions]

    def get_adjacent_positions(self):
        return self.get_directional_adjacent_positions(forward=True) \
            + ((self.get_directional_adjacent_positions(forward=False) if self.king else []))

    def get_column(self):
        return (self.position - 1) % self.board.width

    def get_row(self):
        return self.get_row_from_position(self.position)

    def is_on_enemy_home_row(self):
        return self.get_row() \
            == self.get_row_from_position((1 if self.other_player
                == 1 else self.board.position_count))

    def get_row_from_position(self, position):
        return ceil(position / self.board.width) - 1

    def get_directional_adjacent_positions(self, forward):
        positions = []
        current_row = self.get_row()
        next_row = current_row + ((1 if self.player == 1 else -1)) \
            * ((1 if forward else -1))

        if not next_row in self.board.position_layout:
            return []

        next_column_indexes = self.get_next_column_indexes(current_row,
                self.get_column())

        return [self.board.position_layout[next_row][column_index]
                for column_index in next_column_indexes]

    def get_next_column_indexes(self, current_row, current_column):
        column_indexes = ([current_column, current_column
                          + 1] if current_row % 2
                          == 0 else [current_column - 1,
                          current_column])

        return filter(lambda column_index: column_index >= 0 \
                      and column_index < self.board.width,
                      column_indexes)

    def __setattr__(self, name, value):
        super(Piece, self).__setattr__(name, value)

        if name == 'player':
            self.other_player = (1 if value == 2 else 2)
            
            
class BoardSearcher:

	def build(self, board):
		self.board = board
		self.uncaptured_pieces = list(filter(lambda piece: not piece.captured, board.pieces))
		self.open_positions = []
		self.filled_positions = []
		self.player_positions = {}
		self.player_pieces = {}
		self.position_pieces = {}

		self.build_filled_positions()
		self.build_open_positions()
		self.build_player_positions()
		self.build_player_pieces()
		self.build_position_pieces()

	def build_filled_positions(self):
		self.filled_positions = reduce((lambda open_positions, piece: open_positions + [piece.position]), self.uncaptured_pieces, [])

	def build_open_positions(self):
		self.open_positions = [position for position in range(1, self.board.position_count) if not position in self.filled_positions]

	def build_player_positions(self):
		self.player_positions = {
			1: reduce((lambda positions, piece: positions + ([piece.position] if piece.player == 1 else [])), self.uncaptured_pieces, []),
			2: reduce((lambda positions, piece: positions + ([piece.position] if piece.player == 2 else [])), self.uncaptured_pieces, [])
		}

	def build_player_pieces(self):
		self.player_pieces = {
			1: reduce((lambda pieces, piece: pieces + ([piece] if piece.player == 1 else [])), self.uncaptured_pieces, []),
			2: reduce((lambda pieces, piece: pieces + ([piece] if piece.player == 2 else [])), self.uncaptured_pieces, [])
		}

	def build_position_pieces(self):
		self.position_pieces = {piece.position: piece for piece in self.uncaptured_pieces}

	def get_pieces_by_player(self, player_number):
		return self.player_pieces[player_number]

	def get_positions_by_player(self, player_number):
		return self.player_positions[player_number]

	def get_pieces_in_play(self):
		return self.player_pieces[self.board.player_turn] if not self.board.piece_requiring_further_capture_moves else [self.board.piece_requiring_further_capture_moves]

	def get_piece_by_position(self, position):
		return self.position_pieces.get(position)


class BoardInitializer:

	def __init__(self, board):
		self.board = board

	def initialize(self):
		self.build_position_layout()
		self.set_starting_pieces()

	def build_position_layout(self):
		self.board.position_layout = {}
		position = 1

		for row in range(self.board.height):
			self.board.position_layout[row] = {}

			for column in range(self.board.width):
				self.board.position_layout[row][column] = position
				position += 1

	def set_starting_pieces(self):
		pieces = []
		starting_piece_count = self.board.width * self.board.rows_per_user_with_pieces
		player_starting_positions = {
			1: list(range(1, starting_piece_count + 1)),
			2: list(range(self.board.position_count - starting_piece_count + 1, self.board.position_count + 1))
		}

		for key, row in self.board.position_layout.items():
			for key, position in row.items():
				player_number = 1 if position in player_starting_positions[1] else 2 if position in player_starting_positions[2] else None

				if (player_number):
					pieces.append(self.create_piece(player_number, position))

		self.board.pieces = pieces

	def create_piece(self, player_number, position):
		piece = Piece()
		piece.player = player_number
		piece.position = position
		piece.board = self.board

		return piece


class Board:

	def __init__(self):
		self.player_turn = 1
		self.width = 4
		self.height = 8
		self.position_count = self.width * self.height
		self.rows_per_user_with_pieces = 3
		self.position_layout = {}
		self.piece_requiring_further_capture_moves = None
		self.previous_move_was_capture = False
		self.searcher = BoardSearcher()
		BoardInitializer(self).initialize()

	def count_movable_player_pieces(self, player_number = 1):
		return reduce((lambda count, piece: count + (1 if piece.is_movable() else 0)), self.searcher.get_pieces_by_player(player_number), 0)

	def get_possible_moves(self):
		capture_moves = self.get_possible_capture_moves()

		return capture_moves if capture_moves else self.get_possible_positional_moves()

	def get_possible_capture_moves(self):
		return reduce((lambda moves, piece: moves + piece.get_possible_capture_moves()), self.searcher.get_pieces_in_play(), [])

	def get_possible_positional_moves(self):
		return reduce((lambda moves, piece: moves + piece.get_possible_positional_moves()), self.searcher.get_pieces_in_play(), [])

	def position_is_open(self, position):
		return not self.searcher.get_piece_by_position(position)

	def create_new_board_from_move(self, move):
		new_board = deepcopy(self)

		if move in self.get_possible_capture_moves():
			new_board.perform_capture_move(move)
		else:
			new_board.perform_positional_move(move)

		return new_board

	def perform_capture_move(self, move):
		self.previous_move_was_capture = True
		piece = self.searcher.get_piece_by_position(move[0])
		originally_was_king = piece.king
		enemy_piece = piece.capture_move_enemies[move[1]]
		enemy_piece.capture()
		self.move_piece(move)
		further_capture_moves_for_piece = [capture_move for capture_move in self.get_possible_capture_moves() if move[1] == capture_move[0]]

		if further_capture_moves_for_piece and (originally_was_king == piece.king):
			self.piece_requiring_further_capture_moves = self.searcher.get_piece_by_position(move[1])
		else:
			self.piece_requiring_further_capture_moves = None
			self.switch_turn()

	def perform_positional_move(self, move):
		self.previous_move_was_capture = False
		self.move_piece(move)
		self.switch_turn()

	def switch_turn(self):
		self.player_turn = 1 if self.player_turn == 2 else 2

	def move_piece(self, move):
		self.searcher.get_piece_by_position(move[0]).move(move[1])
		self.pieces = sorted(self.pieces, key = lambda piece: piece.position if piece.position else 0)

	def is_valid_row_and_column(self, row, column):
		if row < 0 or row >= self.height:
			return False

		if column < 0 or column >= self.width:
			return False

		return True

	def __setattr__(self, name, value):
		super(Board, self).__setattr__(name, value)

		if name == 'pieces':
			[piece.reset_for_new_board() for piece in self.pieces]

			self.searcher.build(self)

class Game:

    def __init__(self):
        self.board = Board()
        self.moves = []
        self.consecutive_noncapture_move_limit = 40
        self.moves_since_last_capture = 0
        self.black_numbered_on_board = [i for i in range(1, 33)]
        
    def load_custom_board(self, input_string, player_turn):
        # Converting the input board string to a list of lists
        self.board.player_turn = player_turn
        input_string = input_string.split(',')
        print("Loading board from input string...")
        self.count_pieces = 0
        for index in range(len(input_string)):
            if(input_string[index] == '_'):
                continue
            elif(input_string[index] == 'x' or input_string[index] == 'X' or input_string[index] == 'o' or input_string[index] == 'O'):
                if(input_string[index] == 'x'):
                    self.board.pieces[self.count_pieces].position = self.black_numbered_on_board[index]
                    self.board.pieces[self.count_pieces].player = 1
                    self.board.pieces[self.count_pieces].other_player = 2
                    self.board.pieces[self.count_pieces].is_king = False
                    self.board.pieces[self.count_pieces].captured = False
                    self.board.pieces[self.count_pieces].get_possible_capture_moves()
                    self.board.pieces[self.count_pieces].get_possible_positional_moves()
                elif(input_string[index] == 'o'):
                    self.board.pieces[self.count_pieces].position = self.black_numbered_on_board[index]
                    self.board.pieces[self.count_pieces].player = 2
                    self.board.pieces[self.count_pieces].other_player = 1
                    self.board.pieces[self.count_pieces].is_king = False
                    self.board.pieces[self.count_pieces].captured = False
                    self.board.pieces[self.count_pieces].get_possible_capture_moves()
                    self.board.pieces[self.count_pieces].get_possible_positional_moves()
                elif(input_string[index] == 'X'):
                    self.board.pieces[self.count_pieces].position = self.black_numbered_on_board[index]
                    self.board.pieces[self.count_pieces].player = 1
                    self.board.pieces[self.count_pieces].other_player = 2
                    self.board.pieces[self.count_pieces].is_king = True
                    self.board.pieces[self.count_pieces].captured = False
                    self.board.pieces[self.count_pieces].get_possible_capture_moves()
                    self.board.pieces[self.count_pieces].get_possible_positional_moves()
                elif(input_string[index] == 'O'):
                    self.board.pieces[self.count_pieces].position = self.black_numbered_on_board[index]
                    self.board.pieces[self.count_pieces].player = 2
                    self.board.pieces[self.count_pieces].other_player = 1
                    self.board.pieces[self.count_pieces].is_king = True
                    self.board.pieces[self.count_pieces].captured = False
                    self.board.pieces[self.count_pieces].get_possible_capture_moves()
                    self.board.pieces[self.count_pieces].get_possible_positional_moves()
                self.count_pieces +=1
     
        self.moves = []
        self.consecutive_noncapture_move_limit = 40
        self.moves_since_last_capture = 0
        self.board.get_possible_moves()
         

    def move(self, move):
        if move not in self.get_possible_moves():
            raise ValueError('The provided move is not possible')

        self.board = self.board.create_new_board_from_move(move)
        self.moves.append(move)
        self.moves_since_last_capture = \
            (0 if self.board.previous_move_was_capture else self.moves_since_last_capture
             + 1)
        
        return self

    def move_limit_reached(self):
        return self.moves_since_last_capture \
            >= self.consecutive_noncapture_move_limit

    def is_over(self):
        return self.move_limit_reached() \
            or not self.get_possible_moves()

    def get_winner(self):
        if self.whose_turn() == 1 \
            and not self.board.count_movable_player_pieces(1):
            return 2
        elif self.whose_turn() == 2 \
            and not self.board.count_movable_player_pieces(2):
            return 1
        else:
            return None

    def get_possible_moves(self):
        return self.board.get_possible_moves()

    def whose_turn(self):
        return self.board.player_turn
    
    def save_current_board(self):
        saving_string = list('_'*32)
        for piece in self.board.pieces:
            if piece.position != None:
                if piece.player == 1:
                    if piece.king == True:
                        saving_string[piece.position-1] = 'X'
                    elif piece.king == False:
                        saving_string[piece.position-1] = 'x'
                elif piece.player == 2:
                    if piece.king == True:
                        saving_string[piece.position-1] = 'O'
                    elif piece.king == False:
                        saving_string[piece.position-1] = 'o'
        joined_string = ",".join(saving_string)
        print(joined_string)
        return joined_string
        