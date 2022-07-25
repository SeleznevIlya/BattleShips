class Ship:

    def __init__(self, length, front_point):
        self.length = length
        self.front_point = front_point

    def dots(self):
        #return
        pass




class BoardOutException:
    pass


class Dots:

    def __init__(self,x , y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dor({self.x}, {self.y})'


class Board:

    def __init__(self):
        pass

    def add_ship(self):
        pass

    def contour(self):
        pass

    def board_output(self):
        pass

    def out(self):
        pass

    def shot(self):
        pass


class Player:

    def __init__(self):
        pass

    def ask(self):
        pass

    def move(self):
        pass


class AI(Player):

    pass


class User(Player):

    pass


class Game:

    def random_board(self):
        pass

    def greet(self):
        pass

    def loop(self):
        pass

    def start(self):
        pass



