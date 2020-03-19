#!/usr/bin/env python3
from game import Game
import random

def generate_game(games=1):
    global cursor,turn

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

        print("game {} ".format(i), end="")
        four.out_csv(res)
        four.reset_game()
        cursor = [5,0]

if __name__ == '__main__':
    cursor, turn, res = [5,0], random.choice([-1, 1]), 0
    four = Game(blank=True)
    generate_game(10000)
