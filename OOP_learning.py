from random import randint


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


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"


class Board:
    """
    Класс для создания доски
    """
    def __init__(self, hide=False, size=6):
        self.size = size
        self.hide = hide

        self.count_destroy_ships = 0

        self.game_field = [["O"] * size for _ in range(size)]

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

        if self.hide: # если hide == True, скрывает все корабли
            field_vision = field_vision.replace("■", "O")
        return field_vision

    def add_ship(self, ship):
        '''
        метод отрисовки корабля на поле
        '''
        for d in ship.dots:#проверяем точки корабля на соответствие условиям
            if self.out(d) or d in self.used_points:#если точка за полем или в списке использованых точек
                raise BoardWrongShipException()#выбросит ошибку
        for d in ship.dots:#пробегаемся по точкам корабля
            self.game_field[d.x][d.y] = "■"#и точку на поле с соответствующими координатами отрисовываем как часть корабля
            self.used_points.append(d)#полученную точку отправляем в список использованных точек

        self.ships.append(ship)#добавляем корабль в список кораблей
        self.contour(ship)#отрисовка контура

    def contour(self, ship, game_status=False):
        """
        Метод для вычисления и отрисовки контура корабля
        """
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
            ]
        for d in ship.dots:# цикл по точкам корабля
            for dx, dy in near:# цикл по сдвигам в списке near
                cur = Dot(d.x + dx, d.y + dy)# получаем точки вокруг корабля
                if not (self.out(cur)) and cur not in self.used_points:# если в пределах поля и не в списке занятых точек
                    if game_status:
                        self.game_field[cur.x][cur.y] = "."# точка около корабля становится '.'
                    self.used_points.append(cur)

    def out(self, away):
        """условие что точка выходит за пределы доски"""
        return not ((0 <= away.x < self.size) and (0 <= away.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.used_points:
            raise BoardUsedException()

        self.used_points.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.game_field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count_destroy_ships += 1
                    self.contour(ship, game_status=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.game_field[d.x][d.y] = "."
        print("Мимо!")
        return False

    def begin(self):
        self.used_points = []


class Player:
    def __init__(self, board, enemy_board):
        self.board = board
        self.enemy_board = enemy_board

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy_board.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            turn = input("Ваш ход: ").split()

            if len(turn) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = turn

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:

    def __init__(self, size=6):
        self.size = size
        player = self.random_board()
        ai = self.random_board()
        ai.hide = True

        self.ai = AI(ai, player)
        self.player = User(player, ai)

    def try_board(self):
        ship_lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for ship_len in ship_lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), ship_len, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board



    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.player.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            print("-" * 20)
            if num % 2 == 0:
                print("Ходит пользователь!")
                repeat = self.player.move()
            else:
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count_destroy_ships == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.player.board.count_destroy_ships == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


start_game = Game()
start_game.start()

