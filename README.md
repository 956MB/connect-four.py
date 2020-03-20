# nn-connect-four

```
Cursor: [5, 0]
                                            this is nothing
○ ○ ○ ○ ○ ○ ○         ○ ○ ○ ○ ○ ○ ○         ┌─┬─┬─┬─┬─┬─┬─┐
○ ○ ○ ○ ○ ○ ○    │    ○ ○ ○ ● ○ ○ ○    │    ├─┼─┼─┼─┼─┼─┼─┤
○ ○ ● ◍ ○ ○ ○    │    ○ ○ ● ◍ ○ ○ ○    │    ├─┼─┼─┼─┼─┼─┼─┤
◍ ● ◍ ● ○ ○ ○    │    ◍ ● ◍ ● ○ ○ ○    │    ├─┼─┼─┼─┼─┼─┼─┤
● ◍ ◍ ◍ ● ○ ○    │    ● ◍ ◍ ◍ ● ○ ○    │    ├─┼─┼─┼─┼─┼─┼─┤
● ◍ ◍ ● ● ◍ ●         ● ◍ ◍ ● ● ◍ ●         ├─┼─┼─┼─┼─┼─┼─┤
                                            └─┴─┴─┴─┴─┴─┴─┘
⭠  ⭢  to move.         WINNER: ●
SPACE to select.
ESC to exit.
```

```
not all arguments implemented yet*

usage: play.py [-h] [-n] [-d DATASET] [-s [{1,2,3}]] [-i] [-l]

optional arguments:
  -h, --help            show this help message and exit
  -n, --net             play against trained neural net
  -d DATASET, --dataset DATASET
                        path to .csv moves dataset to load random game
  -s [{1,2,3}], --style [{1,2,3}]
                        style of Connect Four game. 1, 2 or 3.
  -i, --inputmode       play game with input mode rather than with arrow key
                        movement
  -l, --log             log moves of game to logs/
```

# TODO:

* Add input to take in move and push to the board.
* Add optional looks for the game (see below).
* Finish implementing argument features for play.py:
    * --net, --inputmode, --log

# Looks:

<img width="900" src="https://github.com/Bloumbs/nn-connect-four/blob/master/screenshots/looks.png">
