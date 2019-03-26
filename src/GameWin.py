from SuperCodeLogic import SuperCodeLogic
from Color import Color
import curses
import time


class GameWin:

    def __init__(self, scr):
        self.scr = scr
        self.y, self.x = 31, 38
        self.main_win = curses.newwin(self.y, self.x, 0, 0)
        self.logic = SuperCodeLogic()
        self.color = Color()
        self.input_map = {(ord('w'), ord('k'), 259): self.up_input, (ord('s'), ord('j'), 258): self.down_input,
                          (ord('d'), ord('l'), 261): self.right_input, (ord('a'), ord('h'), 260): self.left_input,
                          (49, 50, 51, 52, 53, 54): self.num_input,
                          (ord(' '), 10): self.enter_input, (ord('q'), 27): self.exit_input}
        self.try_index = 0
        self.try_index_map = {0: 2, 1: 6, 2: 10, 3: 14, 4: 18, 5: 22, 6: 26}
        self.color_index = 0
        self.color_index_map = {0: 4, 1: 9, 2: 14, 3: 19}
        self.hint_start = self.color_index_map[3] + 6
        self.cur_key = 0
        self.color_chr = chr(9608) * 2
        self.white_chr = chr(9633)
        self.black_chr = chr(9632)
        self.char_map = {0: chr(9556), 1: chr(9553), 2: chr(9562), 3: chr(9559), 4: chr(9553), 5: chr(9565)}
        self.horizontal_line = "{}{}".format(chr(9500).ljust(self.x - 1, chr(9472)), chr(9508))
        self.horizontal_line_2 = "{}{}".format(chr(0x255e).ljust(self.x - 1, chr(0x2550)), chr(0x2561))
        self.run = True
        self.win = False
        self.loose = False
        self.next_try = False
        self.solution_draw = False
        self.old_index = (0, 0)

    def setup(self):
        curses.noecho()
        curses.curs_set(0)
        self.main_win.nodelay(False)
        self.main_win.keypad(True)
        self.draw()
        self.render()
        self.logic.create_color_code()

    def draw(self):
        start_y = 4
        self.main_win.box()
        for _ in range(5):
            self.main_win.addstr(start_y, 0, self.horizontal_line)
            start_y += 4
        self.main_win.addstr(start_y, 0, self.horizontal_line_2)

    def render(self):
        if self.win:
            self.draw_hints()
        if self.next_try:
            self.draw_hints()
            self.prep_next_round()

        if not self.win and not self.loose:
            self.draw_next_try()
        else:
            if self.solution_draw:
                if self.win:
                    self.main_win.addstr(0, 16, " win ")
                elif self.loose:
                    self.main_win.addstr(0, 16, " sad ")
                self.main_win.addstr(self.try_index_map[6], 12, "The Solution:")
                for i in range(4):
                    self.main_win.addstr(self.try_index_map[6] + 2, self.color_index_map[i] + 6, self.color_chr,
                                         curses.color_pair(self.logic.color_code[i]))
                    self.main_win.refresh()
                    time.sleep(0.25)
                self.solution_draw = False

        if self.next_try:
            self.next_round()
            self.draw_next_try()

        self.new_move()

    def draw_hints(self):
        cur_hint_index = self.hint_start
        for i, val in enumerate(self.logic.hints_map[self.try_index]):
            if val == 2:
                self.main_win.addstr(self.try_index_map[self.try_index], cur_hint_index, self.black_chr + ' ')
            elif val == 1:
                self.main_win.addstr(self.try_index_map[self.try_index], cur_hint_index, self.white_chr + ' ')
            else:
                self.main_win.addstr(self.try_index_map[self.try_index], cur_hint_index, chr(8728))
            cur_hint_index += 3
            if i == 3:
                self.main_win.addstr(self.try_index_map[self.try_index], cur_hint_index, chr(9474))

    def draw_next_try(self):
        for i in range(4):
            self.main_win.addstr(self.try_index_map[self.try_index], self.color_index_map[i], self.color_chr,
                                 curses.color_pair(self.logic.current_guess[i].get_color()))

    def prep_next_round(self):
        self.try_index += 1
        if self.try_index >= 6:
            self.loose = True
            self.solution_draw = True
            self.next_try = False

    def next_round(self):
        self.next_try = False
        self.color_index = 0
        self.logic.reset_current_guess()

    def new_move(self):
        if not self.win and not self.loose:
            old_y = self.try_index_map[self.old_index[1]] - 1
            old_x = self.color_index_map[self.old_index[0]] - 2
            for i in range(3):
                if i == 1:
                    self.main_win.addstr(old_y, old_x, ' ')
                    self.main_win.addstr(old_y, old_x + 5, ' ')
                else:
                    self.main_win.addstr(old_y, old_x, ' ')
                    self.main_win.addstr(old_y, old_x + 5, ' ')
                    self.main_win.addstr(old_y, old_x + 1, '     ')
                old_y += 1
            cur_y = self.try_index_map[self.try_index] - 1
            cur_x = self.color_index_map[self.color_index] - 2
            for i in range(3):
                if i != 1:
                    self.main_win.addstr(cur_y, cur_x, chr(9552) * 5)
                self.main_win.addstr(cur_y, cur_x, self.char_map[i])
                self.main_win.addstr(cur_y, cur_x + 5, self.char_map[i + 3])
                cur_y += 1
            self.old_index = (self.color_index, self.try_index)

    def input(self):
        self.cur_key = self.main_win.getch()
        for tup in self.input_map:
            if self.cur_key in tup:
                self.input_map[tup]()
                break


    def up_input(self):
        if not self.win and not self.loose:
            self.logic.current_guess[self.color_index].color_up()

    def down_input(self):
        if not self.win and not self.loose:
            self.logic.current_guess[self.color_index].color_down()

    def right_input(self):
        if not self.win and not self.loose:
            if self.color_index < 3:
                self.color_index += 1

    def left_input(self):
        if not self.win and not self.loose:
            if self.color_index > 0:
                self.color_index -= 1

    def num_input(self):
        if not self.win and not self.loose:
            num = self.cur_key % 6
            if num == 0:
                num = 6
            self.logic.current_guess[self.color_index].set_color(num)

    def enter_input(self):
        if not self.win and not self.loose:
            if not self.logic.check_guess():
                pass
            elif not self.logic.check_win(self.try_index):
                self.next_try = True
            else:
                self.win = True
                self.solution_draw = True

    def exit_input(self):
        self.run = False

    def game_loop(self):
        while self.run:
            self.input()
            self.render()
