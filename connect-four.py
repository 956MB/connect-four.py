#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
from __future__ import print_function
import numpy as np
import os, csv, sys, random, time, string
import shutil
import os, termios, tty
import argparse
from time import sleep
from bitmap import Bitmap

class Connect4(object):
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

    def pick_random(self, turn):
        avaliable = self.get_open_cols()
        x = random.choice(avaliable)
        for y in range(5, 0, -1):
            piece = [y, x]
            spot = self.board[piece[0]][piece[1]]
            if spot == 0:
                win = self.push_piece([piece, turn])
                if win[0] != 0:
                    winning_pieces = four.get_winning_position(piece, win[0], win[1])
                    four.draw_board(piece, turn, win[0], winning_pieces)
                else:
                    break

    def get_open_cols(self):
        cols = [[[i,x] for i in range(0,6)] for x in range(0,7)]
        open_cols = [i for i in range(7) if not self.check_full(cols[i])]
        return open_cols

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
        flat_moves = [''.join(list(map(str, list(i)))) for i in self.moves]

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


def play_console():
    global cursor,turn

    four.draw_board(cursor, turn)
    try:
        while True:
            k = getkey()
            if k == 'left':
                lspot = four.check_next_column(cursor, "left")
                cursor = lspot
                four.draw_board(cursor, turn)
            elif k == 'right':
                rspot = four.check_next_column(cursor, "right")
                cursor = rspot
                four.draw_board(cursor, turn)
            elif k == 'space':
                win = four.push_piece([cursor,turn])
                if win[0] != 0:
                    if args["log"]:
                        now = datetime.now()
                        timestring = now.strftime("%m-%d-%Y-%H%M%S-moves")
                        four.out_csv(win, "logs/{}.csv".format(timestring), "w")

                    winning_pieces = four.get_winning_position(cursor, win[0], win[1])
                    four.draw_board(cursor, turn, win[0], winning_pieces)

                four.draw_board(cursor, turn)
                turn = -1 if turn == 1 else 1

                if play_random:
                    four.pick_random(turn)
                    turn = -1 if turn == 1 else 1
                    four.draw_board(cursor, turn)

            elif k == 'esc':
                os.system('stty sane')
                sys.exit()

    except (KeyboardInterrupt, SystemExit):
        os.system('stty sane')
        sys.exit()

def getkey():
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    try:
        while True:
            b = os.read(sys.stdin.fileno(), 3).decode()
            if len(b) == 3: k = ord(b[2])
            else: k = ord(b)

            key_mapping = { 27:'esc', 32:'space', 68:'left', 67:'right' }
            return key_mapping.get(k, chr(k))

    except Exception: sys.exit()
    finally: termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description="Play Connect Four in the terminal. Written in Python.")
    opt = ap._action_groups.pop()
    req = ap.add_argument_group('required arguments')
    opt.add_argument("-V","--version",action="store_true",help="show script version")
    opt.add_argument("-n","--net",action="store_true",help="play against trained neural net")
    opt.add_argument("-r","--random",action="store_true",help="play against random moves")
    opt.add_argument("-d","--dataset",help="path to .csv moves dataset to load random game")
    opt.add_argument("-s","--style",const=1,type=int,choices=range(1,4),nargs="?",help="style of Connect Four game. 1, 2 or 3.")
    opt.add_argument("-l","--log",action="store_true",help="log moves of game to logs/")
    ap._action_groups.append(opt)
    args = vars(ap.parse_args())

    mode, path, sep, play_random = True, None, " ", False
    seperators = {1:" ", 2:"|", 3:"("}
    cursor, turn = [5,0], random.choice([-1, 1])
    if args["version"]: sys.exit("v1.0.0")
    if args["random"]: play_random = True
    if args["style"]: sep = seperators[args["style"]]
    if args["dataset"]: mode, path = False, args["dataset"]

    four = Connect4(mode=mode, load=path, sep=sep, starter=turn)
    play_console()