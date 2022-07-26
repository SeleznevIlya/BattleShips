class BoardOutException:
    def __str__(self):
        print('Вы выбрали клетку за пределом поля!')


class ShipPositionError():
    def __str__(self):
        print('Некорректное положение корабля')

class Dot(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot({self.x}, {self.y})'


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


class Board:
    """
    Метод для создания доски
    """
    def __init__(self, size = 6, hide = False):
        self.size = size
        self.hide = hide

        self.count_destroy_ships = 0

        self.game_field = [['0']*size for _ in range(size)]

        self.used_points = []
        self.ships = []

    '''
    Метод печати игровой доски в консоль
    '''
    def __str__(self):
        field_vision = ""
        field_vision += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.game_field):
            field_vision += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hide: #если hide == True, скрывает все корабли
            field_vision = field_vision.replace('■', 'O')
        return field_vision

    """
    Метод добавления кораблей на игровую доску
    """
    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.used_points:
                raise ShipPositionError()
        for d in ship.dots:
            self.game_field[d.x][d.y] = '■'
            self.used_points.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        """
        Метод для вычисления и отрисовки контура корабля
        """
        near = [
            (-1, -1), (1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (-1, 0), (1, 1),
        ]
        for d in ship.dots:#цикл по точкам корабля
            for dx, dy in near:#цикл по сдвигам в списке near
                cur = Dot(d.x + dx, d.y + dy)#получаем точки вокруг корабля
                #self.game_field[cur.x][cur.y] = '+'
                if not(self.out(cur)) and not cur in self.used_points:#если в пределах поля и не в списке занятых точек
                    if verb:
                        self.game_field[cur.x][cur.y] = '.'#точка около корабля становится '.'
                    self.used_points.append(cur)

    def out(self, away):
        """условие что точка выходит за пределы доски"""
        return not((0 <= away.x <= self.size) and (0 <= away.y <= self.size))

    def shot(self):
        pass


a = Board()
b = Ship(Dot(1, 2), 3, 1)
#c = Ship(Dot(0, 0), 3, 1)

print(a.add_ship(b))
#print(a.add_ship(c ))
print(a)
