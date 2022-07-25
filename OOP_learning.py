class Ship:
    def __init__(self, front_point, length_ship, rotation):
        self.front_point = front_point
        self.length_ship = length_ship
        self.rotation = rotation
        self.lives = length_ship

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length_ship):
            cur_x = self.front_point.x
            cur_y = self.front_point.y

            if self.rotation == 0:
                cur_x += i

            elif self.rotation == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots




class BoardOutException:
    def __str__(self):
        print('Вы выбрали клетку за пределом поля!')



class Dot(object):

    def __init__(self,x , y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dor({self.x}, {self.y})'


class Board:

    def __init__(self, size = 6, hide = False):
        self.size = size
        self.hide = hide

        self.count_destroy_ships = 0

        self.game_field = [['0']*size for _ in range(size)]

        self.used_points = []
        self.ships = []

    def __str__(self):
        field_vision = ""
        field_vision += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.game_field):
            field_vision += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hide:
            field_vision = field_vision.replace('■', 'O')
        return field_vision

    def add_ship(self):
        pass

    def contour(self):
        pass

    """@property
    def board_output(self):
        return self.game_field"""

    def out(self, away):
        """условие что точка выходит за пределы доски"""
        return not((0 <= away.x <= self.size) and (0 <= away.y <= self.size))

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



