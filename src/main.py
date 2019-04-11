import argparse
import os
import curses
from functools import partial
from GameWin import GameWin


def main(args, scr):
    game = GameWin(scr, args.lastchance)
    game.setup()
    game.game_loop()


def shorter_esc_delay():
    os.environ.setdefault('ESCDELAY', '25')


if __name__ == '__main__':
    shorter_esc_delay()

    parser = argparse.ArgumentParser(prog='tool',
                                     formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50))
    parser.add_argument("-a", "--lastchance", help="activates alternative game mode", action="store_true")
    args = parser.parse_args()

    curses.wrapper(partial(main, args))
