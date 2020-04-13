# -*- coding: utf-8 -*- 
from __future__ import print_function
import numpy as np
import os, csv, sys
from bitmap import Bitmap

class Game(object):
    def __init__(self, mode=True, load=None, sep=" ", starter=1):
        self.board = np.zeros((6,7), dtype=int)
        self.starter = starter
        self.moves, self.load = [], load
        self.pieces = {0:"\033[90m●\033[0m", 1:"\033[31m●\033[0m", -1:"\033[93m●\033[0m"}
        if sep == " ": self.front, self.middle, self.back = "", " ", ""
        elif sep == "|": self.front, self.middle, self.back = " \033[34m|\033[0m", "", "\033[34m|\033[0m"
        elif sep == "(": self.front, self.middle, self.back = " ", "\033[34m(\033[0m", "\033[34m)\033[0m"
        if not mode: self.load_random_game()

    def reset_game(self, new_turn):
        self.board = np.zeros((6,7), dtype=int)
        self.moves = []
        self.starter = new_turn

    def push_piece(self, piece):
        self.board[piece[0][0]][piece[0][1]] = piece[1]
        self.moves.append(tuple(piece[0]))
        win = self.check_winner()
        if win[0] != 0: return win
        return [0]

    def load_random_game(self):
        with open(self.load, newline='') as file:
            reader = csv.reader(file)
            file.seek(np.random.randint(sum(1 for row in reader)))
            file.readline()
            random_game = file.readline()
            if len(random_game) == 0:
                f.seek(0)
                random_game = f.readline()
            # random_game = np.asarray([int(float(i)) for i in random_game.split(',')[:-1]])
            # random_game = np.reshape(random_game, (-1,7))
        # return random_game

        turn = int(random_game.split(',')[0])
        moves = random_game.split(',')[1:-1]
        moves = [list(map(int, list(i))) for i in moves]
        for place in moves:
            res = self.push_piece([place,turn])
            if res[0] != 0: self.draw_board(place, turn, res[0])
            turn = -1 if turn == 1 else 1
        self.draw_board(winner=res[0])

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
        if winner[0] != 0: return winner
        return [0]
    
    def get_winning_position(self, cursor, winner, direction):
        if direction == '--':
            for i in range(0, 4):
                h = [[cursor[0], i] for i in range(i, i+4)]
                if all(v == winner for v in [self.board[i[0]][i[1]] for i in h]):
                    return h

        elif direction == '|':
            for i in range(0, 3):
                v = [[i, cursor[1]] for i in range(i, i+4)]
                if all(v == winner for v in [self.board[i[0]][i[1]] for i in v]):
                    return v

        elif direction == '\\':
            for i in range(5-cursor[0]):
                cursor[0], cursor[1] = cursor[0]+1, cursor[1]+1
            for i in range(3):
                dl = [[cursor[0]-i, cursor[1]-i] for i in range(0, 4)]
                if all(v == winner for v in [self.board[i[0]][i[1]] for i in dl]): return dl
                cursor[0], cursor[1] = cursor[0]-1, cursor[1]-1

        elif direction == '/':
            for i in range(5-cursor[0]):
                cursor[0], cursor[1] = cursor[0]+1, cursor[1]-1
            for i in range(3):
                dr = [[cursor[0]-i, cursor[1]+i] for i in range(0, 4)]
                if all(v == winner for v in [self.board[i[0]][i[1]] for i in dr]): return dr
                cursor[0], cursor[1] = cursor[0]-1, cursor[1]+1

    def out_csv(self, winner, path, mode):
        # flat_board = self.board.flatten()
        flat_moves = [''.join(list(map(str, list(i)))) for i in self.moves]

        # with open(path, mode, newline='') as csvfile:
            # np.append(flat_board, winner)
            # writer = csv.writer(csvfile)
            # writer.writerow(flat_board)
            # print("board written to custom-datasets/test-output-board.csv")

        with open(path, mode, newline='') as csvfile:
            flat_moves.insert(0, self.starter)
            flat_moves.append(winner)
            writer = csv.writer(csvfile)
            writer.writerow(flat_moves)

    def draw_board(self, cursor=[5,0], turn=1, winner=None, winning_pieces=None):
        os.system('clear')
        print()

        for row_index, row in enumerate(self.board):
            print("{}".format(self.front), end="")
            for col_index, item in enumerate(row):
                current = [row_index, col_index]
                if winning_pieces is None:
                    if current == cursor:
                        if winner: print("{}{}".format(self.middle, self.pieces[item]), end="{}".format(self.back))
                        else: print("{}{}".format(self.middle, self.pieces[1]), end="{}".format(self.back)) if turn == 1 else print("{}{}".format(self.middle, self.pieces[-1]), end="{}".format(self.back))
                    else:
                        print("{}{}".format(self.middle, self.pieces[item]), end="{}".format(self.back))
                else:
                    if current in winning_pieces:
                        print("{}{}".format(self.middle, self.pieces[winner]), end="{}".format(self.back))
                    else:
                        print("{}{}".format(self.middle, self.pieces[0]), end="{}".format(self.back))
            print()

        if winner is None:
            print("\n ⭠  ⭢  to move.")
            print(" SPACE to select.")
            print(" ESC to exit.\n")
        else:
            print("\n   WINNER: {}\n".format(self.pieces[winner]))
            sys.exit()