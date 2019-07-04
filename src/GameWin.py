from SuperCodeLogic import SuperCodeLogic
from Color import Color
import curses
import time


class GameWin:

    def __init__(self, scr, alternativ):
        # the screen obj
        self.scr = scr
        # the magic size of the window
        self.y, self.x = 31, 38
        # creates the game window
        self.win = curses.newwin(self.y, self.x, 0, 0)
        # instance of the Logic class
        self.logic = SuperCodeLogic()
        # instance of the Color class
        self.color = Color()
        # all available inputs as key's and the values are the functions they trigger
        self.input_map = {(ord('w'), ord('k'), 259): self.up_input, (ord('s'), ord('j'), 258): self.down_input,
                          (ord('d'), ord('l'), 261): self.right_input, (ord('a'), ord('h'), 260): self.left_input,
                          (49, 50, 51, 52, 53, 54): self.num_input,(ord(' '), 10): self.enter_input,
                          (ord('r'),): self.reset_input, (ord('q'), 27): self.exit_input}
        # is the index to the try_index_map witch defines where on the x-axis the try's are located
        self.try_index = 0
        self.try_index_map = {0: 2, 1: 6, 2: 10, 3: 14, 4: 18, 5: 22, 6: 26}
        # is the index to the color_index_map witch defines where on the y-axis the single guess is located
        self.color_index = 0
        self.color_index_map = {0: 4, 1: 9, 2: 14, 3: 19}
        # defines where on the y-axis the hints are located
        self.hint_start = self.color_index_map[3] + 6
        # stores current input
        self.cur_key = 0
        # the symbol that presents the color
        self.color_chr = chr(9608) * 2
        # the char that presents an almost hit
        self.white_chr = chr(9633)
        # the char that presents a perfect hit
        self.black_chr = chr(9632)
        # the char that presents a none hit
        self.blank_chr = chr(8728)
        # contains all char's needed to build cursor
        # (0 to 5 are in specific order needed for redraw_cursor_pos 6 is there for storage reasons)
        self.cursor_chars = {0: chr(9556), 1: chr(9553), 2: chr(9562), 3: chr(9559), 4: chr(9553), 5: chr(9565),
                             6: chr(9552)}
        # some string's that are used to build interface
        self.horizontal_line = "{}{}".format(chr(9500).ljust(self.x - 1, chr(9472)), chr(9508))
        self.horizontal_line_2 = "{}{}".format(chr(0x255e).ljust(self.x - 1, chr(0x2550)), chr(0x2561))
        # flag that runs the main loop
        self.run = True
        # prevents the delay of the draw_game_ending() happening on every input after a win or lose
        self.draw_solution = True
        # is the position where the cursor is located
        self.old_cursor_pos = (0, 0)
        if alternativ:
            self.game_setup = self.alt_game_setup
        else:
            self.game_setup = self.normal_game_setup

    def setup(self):
        # set's curses to no echo mode
        curses.noecho()
        # set's cursor visibility to none visible
        curses.curs_set(0)
        # activates delayed input
        self.win.nodelay(False)
        # activates arrow key's
        self.win.keypad(True)
        # self.normal_game_setup()
        self.game_setup()

    # draws the interface (normal game)
    def normal_game_setup(self):
        self.logic.create_color_code()
        self.draw()
        self.render()

    # draws the interface (alternative game)
    def alt_game_setup(self):
        self.logic.altgamemode_setup()
        self.draw()
        self.draw_altgamemode()

    # draws the interface (lines)
    def draw(self):
        start_y = 4
        self.win.box()
        for _ in range(5):
            self.win.addstr(start_y, 0, self.horizontal_line)
            start_y += 4
        self.win.addstr(start_y, 0, self.horizontal_line_2)

    # draws the first 5 color trys and hints for the alternative game mode
    def draw_altgamemode(self):
        for i in range(5):
            for (j, field) in enumerate(self.logic.guesses_map[self.try_index]):
                self.win.addstr(self.try_index_map[self.try_index], self.color_index_map[j], self.color_chr,
                                     curses.color_pair(field.get_color()))
            self.draw_hints()
            self.try_index += 1
        self.redraw_colors()
        self.redraw_cursor()

    # draws colors / hints / end game things
    def render(self):
        if self.logic.next_try:
            self.draw_hints()
            self.next_round()
        if self.logic.win or self.logic.lose:
            if self.draw_solution:
                self.draw_hints()
                self.draw_game_ending()

        self.redraw_colors()
        self.redraw_cursor()

    def draw_hints(self):
        cur_hint_index = self.hint_start
        for i, val in enumerate(self.logic.hints_map[self.try_index]):
            if val == 2:
                self.win.addstr(self.try_index_map[self.try_index], cur_hint_index, self.black_chr + ' ')
            elif val == 1:
                self.win.addstr(self.try_index_map[self.try_index], cur_hint_index, self.white_chr + ' ')
            else:
                self.win.addstr(self.try_index_map[self.try_index], cur_hint_index, self.blank_chr)
            cur_hint_index += 3
            if i == 3:
                # prints a wall piece at the end to prevent a bug in curses where the unicode char's are cut off if no
                # symbol follows
                self.win.addstr(self.try_index_map[self.try_index], cur_hint_index, chr(9474))

    # updates colors and draws the color chars on next try
    def redraw_colors(self):
        for i in range(4):
            self.win.addstr(self.try_index_map[self.try_index], self.color_index_map[i], self.color_chr,
                                 curses.color_pair(self.logic.current_guess[i].get_color()))

    # draws everything after the game finished
    def draw_game_ending(self):
        if self.logic.win:
            self.win.addstr(0, 16, " win ")
        elif self.logic.lose:
            self.win.addstr(0, 16, " sad ")
        self.win.addstr(self.try_index_map[6], 12, "The Solution:")
        for i in range(4):
            self.win.addstr(self.try_index_map[6] + 2, self.color_index_map[i] + 6, self.color_chr,
                                 curses.color_pair(self.logic.color_code[i]))
            self.win.refresh()
            time.sleep(0.25)
        self.draw_solution = False

    # resets some things to init next round
    def next_round(self):
        self.try_index += 1
        self.logic.next_try = False
        self.color_index = 0
        self.logic.reset_current_guess()

    # removes and redraws the cursor
    def redraw_cursor(self):
        if not (self.logic.win or self.logic.lose):
            old_y = self.try_index_map[self.old_cursor_pos[1]] - 1
            old_x = self.color_index_map[self.old_cursor_pos[0]] - 2
            # removes old cursor
            for i in range(3):
                if i == 1:
                    self.win.addstr(old_y, old_x, ' ')
                    self.win.addstr(old_y, old_x + 5, ' ')
                else:
                    self.win.addstr(old_y, old_x, ' ')
                    self.win.addstr(old_y, old_x + 5, ' ')
                    self.win.addstr(old_y, old_x + 1, '     ')
                old_y += 1
            cur_y = self.try_index_map[self.try_index] - 1
            cur_x = self.color_index_map[self.color_index] - 2
            # prints new cursor
            for i in range(3):
                if i != 1:
                    self.win.addstr(cur_y, cur_x, self.cursor_chars[6] * 5)
                self.win.addstr(cur_y, cur_x, self.cursor_chars[i])
                self.win.addstr(cur_y, cur_x + 5, self.cursor_chars[i + 3])
                cur_y += 1
            self.old_cursor_pos = (self.color_index, self.try_index)

    # handles input
    def input(self):
        self.cur_key = self.win.getch()
        for tup in self.input_map:
            if self.cur_key in tup:
                self.input_map[tup]()
                break

    # cycles colors
    def up_input(self):
        if not (self.logic.win or self.logic.lose):
            self.logic.current_guess[self.color_index].color_up()

    # cycles colors
    def down_input(self):
        if not (self.logic.win or self.logic.lose):
            self.logic.current_guess[self.color_index].color_down()

    # moves cursor
    def right_input(self):
        if not (self.logic.win or self.logic.lose):
            if self.color_index < 3:
                self.color_index += 1

    # moves cursor
    def left_input(self):
        if not (self.logic.win or self.logic.lose):
            if self.color_index > 0:
                self.color_index -= 1

    # sets color
    def num_input(self):
        if not (self.logic.win or self.logic.lose):
            num = self.cur_key % 6
            if num == 0:
                num = 6
            self.logic.current_guess[self.color_index].set_color(num)

    # resets game state
    def reset_input(self):
        self.logic = SuperCodeLogic()
        self.win.clear()
        self.try_index = 0
        self.draw_solution = True
        self.game_setup()

    # validates current guess
    def enter_input(self):
        if not (self.logic.win or self.logic.lose):
            self.logic.check_win(self.try_index)

    # stops main loop
    def exit_input(self):
        self.run = False

    def game_loop(self):
        while self.run:
            self.input()
            self.render()
