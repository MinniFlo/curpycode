from GameWin import GameWin
import curses


def main(scr):
    game = GameWin(scr)
    game.setup()
    game.game_loop()


if __name__ == '__main__':
    curses.wrapper(main)
