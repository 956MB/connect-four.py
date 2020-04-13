#!/usr/bin/env python3
from game import Game
import random, sys

def generate_game(games=1):
    global cursor,turn
    save_path = "custom-datasets/test-output-moves.csv"

    for i in range(games):
        for _ in range(42):
            direc, rand = random.choice(["left", "right"]), random.randrange(1, 7)
            cursor[1] = rand
            spot = four.check_next_column(cursor, direc)
            cursor = spot
            res = four.push_piece([cursor,turn])
            if res != 0:
                break
            turn = -1 if turn == 1 else 1

        print("game {} logged to {}".format(i, save_path))
        four.out_csv(res, save_path, "a")
        cursor, turn = [5,0], random.choice([-1, 1])
        four.reset_game(turn)

if __name__ == '__main__':
    cursor, turn, res = [5,0], random.choice([-1, 1]), 0
    four = Game(mode=True, starter=turn)
    try:
        generate_game(sys.argv[1])
    except IndexError:
        print("game amount not given")
