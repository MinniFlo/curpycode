import curses

class InfoWin:

    def __init__(self, window_messure):
        self.win = curses.newwin(window_messure[0] + 1, 85, 0, window_messure[1])
        # the char that presents a code piece
        self.color_chr = chr(9608) * 2
        # the char that presents an almost hit
        self.white_chr = chr(9633)
        # the char that presents a perfect hit
        self.black_chr = chr(9632)
        # the char that presents a none hit
        self.blank_chr = chr(8728)
        # arrow symbols
        self.arrow_left = chr(8592)
        self.arrow_up = chr(8593)
        self.arrow_right = chr(8594)
        self.arrow_down = chr(8595)
        self.info_y, self.info_x = (1, 1)
        # the string that contains informations of the game
        self.info_str = " Movement\n" \
                        "   ~ w,a,s,d/h,j,k,l/{left},{up},{right},{down}:\n" \
                        "     navigate sideways and cycle the colors of the current selection\n\n" \
                        "   ~ 1,2,3,4,5,6:\n" \
                        "     set a specific color to the current selection\n\n" \
                        "   ~ enter/space:\n" \
                        "     confirm your current choice of colors\n\n" \
                        "   ~ r:\n" \
                        "     restart the game\n\n" \
                        " Gameplay\n" \
                        "   The goal is to guess the color code within six guesses correctly.\n\n" \
                        "   The color code can consist of any combination of these colors:\n\n" \
                        "     ##  ##  ##  ##  ##  ##\n\n" \
                        "   You can only confirm a guess if you fill all slots with a color\n\n" \
                        "   If your guess is not correct you will get hints:\n\n" \
                        "     ~ {black} one of your slots is identical with the color code\n\n" \
                        "     ~ {white} one of your slots holds a color that is in the color code,\n" \
                        "         but not in the right position\n\n" \
                        "     ~ {blank} one of your slots holds a color that is not in the color code\n" \
            .format(left=self.arrow_left, up=self.arrow_up, right=self.arrow_right, down=self.arrow_right,
                    black=self.black_chr, white=self.white_chr, blank=self.blank_chr)

    def draw(self):
        self.win.addstr(1, 0, self.info_str)
        # make headlines bold
        self.win.addstr(1, self.info_x, "MOVEMENT", curses.A_BOLD)
        self.win.addstr(14, self.info_x, "GAMEPLAY", curses.A_BOLD)
        # make key options bold
        self.win.addstr(2, self.info_x, "  ~ w,a,s,d/h,j,k,l/{left},{up},{right},{down}:"
                        .format(left=self.arrow_left, up=self.arrow_up, right=self.arrow_right, down=self.arrow_right),
                        curses.A_BOLD)
        self.win.addstr(5, self.info_x, "  ~ 1,2,3,4,5,6:", curses.A_BOLD)
        self.win.addstr(8, self.info_x, "  ~ enter/space:", curses.A_BOLD)
        self.win.addstr(11, self.info_x, "  ~ r:", curses.A_BOLD)
        cur_y, cur_x = 19, 5
        for color in range(1, 7):
            self.win.addstr(cur_y, cur_x, self.color_chr, curses.color_pair(color))
            cur_x += 4
        self.win.refresh()

