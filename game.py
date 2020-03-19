import numpy as np
import os, csv, sys, random
from colorama import Fore, Style
from bitmap import Bitmap

class Game(object):
    def __init__(self, blank=True):
        self.board = np.zeros((6,7), dtype=int) if blank else self.load_random_game()
        self.moves = []
        self.pieces = {0:f"{Fore.WHITE}{Style.DIM}●{Style.RESET_ALL}", 1:f"{Fore.RED}●{Style.RESET_ALL}", -1:f"{Fore.YELLOW}●{Style.RESET_ALL}"}
        self.players = {1:"RED", -1:"YELLOW"}
        if not blank: self.check_winner()

    def reset_game(self):
        self.board = np.zeros((6,7), dtype=int)
        self.moves = []

    def push_piece(self, piece):
        self.board[piece[0][0]][piece[0][1]] = piece[1]
        self.moves.append(tuple(piece[0]))
        win = self.check_winner()
        if win != 0: return win
        return 0

    def load_random_game(self):
        with open('data/c4_game_database.csv', newline='') as file:
            reader = csv.reader(file)
            file.seek(random.randrange(376641))
            file.readline()
            random_game = file.readline()
            if len(random_game) == 0:
                f.seek(0)
                random_game = f.readline()
            random_game = np.asarray([int(float(i)) for i in random_game.split(',')[:-1]])
            random_game = np.reshape(random_game, (-1,7))
        return random_game

    def check_next_column(self, cursor, direction):
        skip = True
        if direction == "right": cursor[1] = 0 if cursor[1] == 6 else cursor[1]+1
        else: cursor[1] = 6 if cursor[1] == 0 else cursor[1]-1
        while skip:
            col = list(reversed([[i, cursor[1]] for i in range(0, 6)]))
            skip = self.check_full(col)
            if skip:
                if direction == "right": cursor[1] = 0 if cursor[1] == 6 else cursor[1]+1
                else: cursor[1] = 6 if cursor[1] == 0 else cursor[1]-1
                continue
            for i in col:
                spot = self.board[i[0]][i[1]]
                if spot == 0: return i

    def check_full(self, column):
        items = [self.board[i[0]][i[1]] for i in column]
        if 0 not in items: return True
        return False

    def check_winner(self):
        winner = Bitmap(self.board.flatten()).check_winner()
        if winner != 0: return winner
        return 0

    def out_csv(self, winner):
        # flat_board = self.board.flatten()
        flat_moves = [''.join(list(map(str, list(i)))) for i in self.moves]

        # with open('custom-datasets/test-output-board.csv', 'a', newline='') as csvfile:
            # np.append(flat_board, winner)
            # writer = csv.writer(csvfile)
            # writer.writerow(flat_board)
            # print("board written to custom-datasets/test-output-board.csv")

        with open('custom-datasets/test-output-moves.csv', 'a', newline='') as csvfile:
            flat_moves.append(winner)
            writer = csv.writer(csvfile)
            writer.writerow(flat_moves)
            print("moves written to custom-datasets/test-output-moves.csv")

    def draw_board(self, cursor=[5,0], turn=1, winner=None):
        os.system('clear')
        if winner is None: print("\n Cursor: {}\n".format(cursor))
        else: print()

        for row_index, row in enumerate(self.board):
            print(" ", end="")
            for col_index, item in enumerate(row):
                current = [row_index, col_index]
                if current == cursor:
                    if winner: print("{}".format(self.pieces[item]), end=" ")
                    else: print("{}".format(self.pieces[1]), end=" ") if turn == 1 else print(self.pieces[-1], end=" ")
                else:
                    print("{}".format(self.pieces[item]), end=" ")
            print()

        if winner is None:
            print("\n ⭠  ⭢  to move.")
            print(" SPACE to select.")
            print(" ESC to exit.\n")
        else:
            print("\n   WINNER: {}\n".format(self.pieces[winner]))
            sys.exit()
