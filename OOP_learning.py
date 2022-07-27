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


class ShipPositionException:
    def __str__(self):
        print('Некорректное положение корабля')


class BoardUsedPointsException:
    def __str__(self):
        print('Невозможно выстрелить в эту точку')


class Dot:

    def __init__(self,x , y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dor({self.x}, {self.y})'


class Board:
    """
    Класс для создания доски
    """
    def __init__(self, size = 6, hide = False):
        self.size = size
        self.hide = hide

        self.count_destroy_ships = 0

        self.game_field = [['0']*size for _ in range(size)]

        self.used_points = []
        self.ships = []

    def __str__(self):
        '''
        Метод печати игровой доски в консоль
        '''
        field_vision = ""
        field_vision += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.game_field):
            field_vision += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hide:
            field_vision = field_vision.replace('■', 'O')
        return field_vision

    def add_ship(self, ship):
        '''
        метод отрисовки корабля на поле
        '''
        for d in ship.dots:#проверяем точки корабля на соответствие условиям
            if self.out(d) or d in self.used_points:#если точка за полем или в списке использованых точек
                raise ShipPositionException()#выбросит ошибку
        for d in ship.dots:#пробегаемся по точкам корабля
            self.game_field[d.x][d.y] = '■'#и точку на поле с соответствующими координатами отрисовываем как часть корабля
            self.used_points.append(d)#полученную точку отправляем в список использованных точек

        self.ships.append(ship)#добавляем корабль в список кораблей
        self.contour(ship)#отрисовка контура

    def contour(self, ship, game_status=False):
        """
        Метод для вычисления и отрисовки контура корабля
        """
        near = [
            (-1, -1), (1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (-1, 0), (1, 1),
        ]
        for d in ship.dots:  # цикл по точкам корабля
            for dx, dy in near:  # цикл по сдвигам в списке near
                cur = Dot(d.x + dx, d.y + dy)  # получаем точки вокруг корабля
                # self.game_field[cur.x][cur.y] = '+'
                if not (self.out(cur)) and cur not in self.used_points:  # если в пределах поля и не в списке занятых точек
                    if game_status:
                        self.game_field[cur.x][cur.y] = '.'  # точка около корабля становится '.'
                    self.used_points.append(cur)

    def out(self, away):
        """условие что точка выходит за пределы доски"""
        return not((0 <= away.x <= self.size) and (0 <= away.y <= self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        '''if d in self.used_points:
            raise BoardUsedPointsException()'''

        self.used_points.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.game_field[d.x][d.y] = 'X'
                if ship.lives == 0:
                    self.count_destroy_ships += 1
                    self.contour(ship, verb=True)
                    print('Корабль убит')
                    return False
                else:
                    print('Корабль ранен')
                    return True

        self.game_field[d.x][d.y] = '.'
        print('Промахнулся')
        return False

    def begin(self):
        self.used_points = []


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

a = Board()
b = Ship(Dot(1, 2), 3, 0)

print(a.add_ship(b))
print(a)

