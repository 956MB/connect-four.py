#!/usr/bin/env python3
from game import Game
import sys, random, tty, os, termios

def play_terminal():
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
                four.push_piece([cursor,turn])
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
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

if __name__ == '__main__':
    cursor, turn = [5,0], random.choice([-1, 1])
    four = Game(blank=True)
    play_terminal()
