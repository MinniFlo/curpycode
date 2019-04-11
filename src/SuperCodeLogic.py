from Field import Field
import random
import curses


class SuperCodeLogic:

    def __init__(self):
        # the solution
        self.color_code = {0: 0, 1: 0, 2: 0, 3: 0}
        # the current try
        self.current_guess = {0: Field(0), 1: Field(0), 2: Field(0), 3: Field(0)}
        # stores all the guesses
        self.guesses_map = {0: [], 1: [], 2: [], 3: [], 4: [],
                            5: []}
        # stores all the hints
        self.hints_map = {0: [], 1: [], 2: [], 3: [], 4: [],
                          5: []}
        # flag that indicates a win
        self.win = False
        # flag that indicates a loose
        self.lose = False
        # flag that indicates weather the next step is allowed
        self.next_try = False

    # creates a new color code
    def create_color_code(self):
        for i in range(4):
            # color numbers ranges from 1 to 6
            self.color_code[i] = random.randrange(1, 7)

    # fills a complete guess in to the guesses_map
    def fill_guesses_map(self, index):
        for field in self.current_guess.values():
            self.guesses_map[index].append(field)

    def reset_current_guess(self):
        for i in range(4):
            self.current_guess[i] = Field(0)

    # checks if the current guess is completely filled with colors
    # has to be called before check_win
    def check_guess(self):
        for field in self.current_guess.values():
            if field.get_color() == 0:
                return False
        return True

    # builds the hints of the current guess and puts it in to the hints_map
    def build_hints(self, index):
        hint_list = []
        # creates a copy of the colorcode and the guess to safely remove values
        check_current_guess = dict()
        check_color_code = self.color_code.copy()
        for (i, field) in enumerate(self.guesses_map[index]):
            check_current_guess[i] = field.get_color()
        # checks the two of exact matches and removes them
        for (k, color) in enumerate(check_current_guess.values()):
            if color == check_color_code[k]:
                hint_list.append(2)
                check_current_guess[k] = 0
                check_color_code[k] = 0
        # checks the two of near matches and removes them
        for (p, guess_color) in enumerate(check_current_guess.values()):
            if guess_color != 0:
                for (j, color) in enumerate(check_color_code.values()):
                    if guess_color == color:
                        hint_list.append(1)
                        check_current_guess[p] = 0
                        check_color_code[j] = 0
                        break
        # fills the hintlist up to length 4 and inserts it into the map
        hint_list += [0] * (4 - len(hint_list))
        self.hints_map[index] = hint_list

    # checks the hints and sets the win/lose/next_try flags
    def check_win(self, index):
        if self.check_guess():
            self.fill_guesses_map(index)
            self.build_hints(index)
            if self.hints_map[index].count(2) == 4:
                self.win = True
                return
            if index >= 5:
                self.lose = True
                return
            self.next_try = True
