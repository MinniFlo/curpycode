from Field import Field
import random
import curses


class SuperCodeLogic:

    def __init__(self):
        self.color_code = {0: 0, 1: 0, 2: 0, 3: 0}
        self.current_guess = {0: Field(), 1: Field(), 2: Field(), 3: Field()}
        self.guesses_map = {0: [], 1: [], 2: [], 3: [], 4: [],
                            5: [], 6: []}
        self.hints_map = {0: [], 1: [], 2: [], 3: [], 4: [],
                          5: [], 6: []}
        self.win = False

    def create_color_code(self):
        for i in range(4):
            rand_int = random.randrange(1, 7)
            self.color_code[i] = rand_int

    def fill_color_map(self, index):
        for i in self.current_guess.values():
            self.guesses_map[index].append(i)

    def reset_current_guess(self):
        for i in range(4):
            self.current_guess[i] = Field()

    def check_guess(self):
        for field in self.current_guess.values():
            if field.get_color() == 0:
                return False
        return True

    def check_win(self, index):
        self.fill_color_map(index)
        hint_list = []
        check_current_guess = self.current_guess.copy()
        check_color_code = self.color_code.copy()
        for i in range(4):
            check_current_guess[i] = self.current_guess[i].get_color()
        for (i, color) in enumerate(check_current_guess.values()):
            if color == check_color_code[i]:
                hint_list.append(2)
                check_current_guess[i] = 0
                check_color_code[i] = 0
        for (i, guess_color) in enumerate(check_current_guess.values()):
            if guess_color != 0:
                for (j, color) in enumerate(check_color_code.values()):
                    if guess_color == color:
                        hint_list.append(1)
                        check_current_guess[i] = 0
                        check_color_code[j] = 0
                        break
        hint_list += [0] * (4 - len(hint_list))
        self.hints_map[index] = hint_list
        for i in hint_list:
            if i != 2:
                return False
        return True



# if __name__ == '__main__':
#     logic = SuperCodeLogic()
#     logic.create_color_code()
#     print(logic.color_code)

