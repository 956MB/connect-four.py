#!/usr/bin/env python3
from game import Game
from datetime import datetime
import sys, random, tty, os, termios
import argparse

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
            elif k == 'esc':
                os.system('stty sane')
                sys.exit()

    except (KeyboardInterrupt, SystemExit):
        os.system('stty sane')

def getkey():
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    try:
        while True:
            b = os.read(sys.stdin.fileno(), 3).decode()
            if len(b) == 3:
                k = ord(b[2])
            else:
                k = ord(b)
            key_mapping = {
                27: 'esc',
                32: 'space',
                68: 'left',
                67: 'right'
            }
            return key_mapping.get(k, chr(k))

    except Exception:
        sys.exit()
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    opt = ap._action_groups.pop()
    req = ap.add_argument_group('required arguments')
    opt.add_argument("-n","--net",action="store_true",
            help="play against trained neural net")
    opt.add_argument("-d","--dataset",
            help="path to .csv moves dataset to load random game")
    opt.add_argument("-s","--style",const=1,type=int,choices=range(1,4),nargs="?",
            help="style of Connect Four game. 1, 2 or 3.")
    opt.add_argument("-l","--log",action="store_true",
            help="log moves of game to logs/")
    ap._action_groups.append(opt)
    args = vars(ap.parse_args())

    mode, path, sep = True, None, " "
    seperators = {1:" ", 2:"|", 3:"("}
    cursor, turn = [5,0], random.choice([-1, 1])
    if args["style"]: sep = seperators[args["style"]]
    if args["dataset"]: mode, path = False, args["dataset"]

    four = Game(mode=mode, load=path, sep=sep, starter=turn)
    play_console()
