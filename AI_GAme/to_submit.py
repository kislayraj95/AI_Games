import numpy as np
from collections import defaultdict
import tkinter as tk

# function to check if the move is valid/legal
def is_move_valid(board, x, y):
    return 0 <= x < board_size and 0 <= y < board_size and board[x][y] == -1

# function to find the list of all moves and return them in ascending order
def find_sorted_move_list(board, x, y, legal_moves):
    move_list = []
    for move in legal_moves: # adding moves from legal moves
        x_after = x + move[0]
        y_after = y + move[1]
        if is_move_valid(board, x_after, y_after): # checking validity of move
            move_list.append([x_after, y_after])

    # sorting the list in ascending order
    move_list_sorted = sorted(move_list, 
                          key=lambda c: sum([is_move_valid(board, c[0] + j[0], c[1] + j[1]) for j in legal_moves]))
    
    return move_list_sorted

# function to save the path followed and coordinates of each point that the knight took in the solution
def saving_path_of_board(board):
    board_path_dict = defaultdict(list)
    for key,item in np.ndenumerate(board):
        board_path_dict[item].append(key) # adding all path-coordinates and key-values in dictionary
    board_path_dict = dict(board_path_dict)
    board_path_dict = dict(sorted(board_path_dict.items())) # sorting the dictionary in ascending order of keys to help with tkinter plotting
    return board_path_dict

# function that runs recursively and checks if there is a solution or not
def find_solution(board, x, y, move_counter, legal_moves):
    if move_counter == board_size * board_size: # to check if limit of 64 has reached
        print(board) # printing board
        # for i in range(board_size): #printing board without brackets
        #     for j in range(board_size):
        #         print("%3d" % board[i][j], end=" ")
        #     print()
        return True # returning true if a solution is found
    # calling function to return the list of all moves in ascending order
    move_list_sorted = find_sorted_move_list(board, x, y, legal_moves) 

    for x_after, y_after in move_list_sorted: # looping over the sorted list, helps speed up the solution finding process
        board[x_after][y_after] = move_counter # updating the board

        if find_solution(board, x_after, y_after, move_counter + 1, legal_moves): # recursion, move_counter is increased by 1
            return True # returning true if a solution is found

        board[x_after][y_after] = -1 # back-tracking if the solution is not correct

    return False # returning false if a solution is not found

class GameBoard(tk.Frame):
    def __init__(self, parent, rows=8, columns=8, size=64, color1="#a7ab90", color2="#0e140c"):
        '''size is the size of a square, in pixels'''
        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.pieces = {}
        canvas_width = columns * size
        canvas_height = rows * size
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="khaki")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)
        # this binding will cause a refresh if the user interactively changes the window size
        self.canvas.bind("<Configure>", self.refresh)
        
    def draw_line(self, x1, y1, x2, y2, width, fill):
        x1 *= self.size
        y1 *= self.size
        x2 *= self.size
        y2 *= self.size
        half = self.size / 2
        self.canvas.create_line(x1+half, y1+half, x2+half, y2+half, width=width, fill=fill)

    def addpiece(self, name, image, row=0, column=0):
        '''Add a piece to the playing board'''
        self.canvas.create_image(0,0, image=image, tags=(name, "piece"), anchor="c")
        self.placepiece(name, row, column)

    def placepiece(self, name, row, column):
        '''Place a piece at the given row/column'''
        self.pieces[name] = (row, column)
        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)
        self.canvas.coords(name, x0, y0)

    def refresh(self, event):
        '''Redraw the board, possibly in response to window being resized'''
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2
        for name in self.pieces:
            self.placepiece(name, self.pieces[name][0], self.pieces[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")
        
        
if __name__ == "__main__":
    # initialising the board
    board_size = 8
    board = np.full((board_size, board_size), fill_value = -1, dtype=int)
    x_initial, y_initial = 0, 0 # setting the initial position of the knight
    board[x_initial][y_initial] = 0 # setting the value of initial position as 0
    # all 8 possible moves of knight at any given position
    legal_moves = ((-1, 2), 
                    (1, 2), 
                    (2, 1), 
                    (2, -1), 
                    (1, -2), 
                    (-1, -2), 
                    (-2, -1), 
                    (-2, 1)
                    )
    print(f"Initial Point:{x_initial, y_initial}")
    solution_exists = find_solution(board, x_initial, y_initial, 1, legal_moves)
    if not solution_exists:
        print("No solution exist!")
    board_path_dict = saving_path_of_board(board)
    print("Path and Coordinates of the solution followed by the Knight:\n", board_path_dict)
    
    # Initialising the chessboard for Tkinter
    root = tk.Tk()
    root.title(f"Knight's Tour Problem with initial point:{x_initial, y_initial}")
    chessboard = GameBoard(root)
    chessboard.pack(side="top", fill="both", expand="true", padx=10, pady=10)
    # Adding the knight's image on the board
    # knight = tk.PhotoImage(file = r"C:\Gfg\knight.png")
    knight = tk.PhotoImage(file = "chess_knight.png")
    chessboard.addpiece("knight", knight, x_initial,y_initial)
    def move_piece(i=0):
        if i < len(board_path_dict)-1:
            cell_1 = board_path_dict[i][0]
            cell_2 = board_path_dict[i+1][0]
            # draw the line
            chessboard.draw_line(cell_1[0], cell_1[1], cell_2[0], cell_2[1], width=4.3, fill='red')
            # move the chess piece
            chessboard.placepiece("knight", cell_2[1], cell_2[0])
            chessboard.after(500, move_piece, i+1)

    # start the chess piece moving
    chessboard.after(500, move_piece)
    root.mainloop()