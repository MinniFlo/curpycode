import curses

def main(scr):
    scr.box()
    win = curses.newwin(3, 3, 0, 0)
    win.box()
    win.getch()

curses.wrapper(main)
