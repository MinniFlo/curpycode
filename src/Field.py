

class Field:

    def __init__(self, color):
        self.color = color

    def color_up(self):
        self.color = (self.color % 6) + 1

    def color_down(self):
        if self.color == 0:
            self.color = 6
        else:
            self.color = ((self.color - 2) % 6) + 1

    def get_color(self):
        return self.color

    def set_color(self, num):
        self.color = num
