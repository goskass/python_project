import random                            #Этот оператор импортирует модуль random, который используется для генерации случайных чисел.

class Ship:                             #Этот класс представляет корабль заданного размера.
    """Этот класс представляет корабль заданного размера. У него есть атрибуты size (размер корабля),
     symbols (список символов, представляющих корабль), и is_sunk (флаг, указывающий, потоплен ли корабль)."""
    
    def __init__(self, size):           #конструктор класса Ship
        self.size = size                #размер корабля
        self.symbols = ["■"] * size     #список символов, представляющих корабль
        self.is_sunk = False            #флаг, указывающий, потоплен ли корабль

class Board:                           #Этот класс представляет игровую доску
    """Этот класс представляет игровую доску. У него есть атрибуты size (размер доски),
    grid (двумерный список, представляющий состояние доски с начальными значениями 'O')
    ships (список для хранения кораблей на доске)."""

    def __init__(self, size):          #конструктор класса Board
        self.size = size               #размер доски
        self.grid = [['O'] * size for _ in range(size)] #двумерный список, представляющий состояние доски с начальными значениями 'O'
        self.ships = []                #список для хранения кораблей на доске

    def print_board(self):            #метод выводит текущее состояние доски
        print("   " + " ".join(str(i) for i in range(1, self.size + 1)))
        for i, row in enumerate(self.grid):
            print(f"{i+1:2} {' '.join(row)}")

    def is_valid_ship_location(self, x, y, ship):  #Проверяет, является ли размещение корабля на координатах (x, y) допустимым
        min_distance = 1

        for existing_ship in self.ships:
            for i, j in existing_ship.position:
                if abs(x - i) <= min_distance and abs(y - j) <= min_distance:
                    return False

        for i in range(ship.size):
            if (
                x + i >= self.size
                or y + i >= self.size
                or self.grid[x + i][y] != "O"
            ):
                return False
            for j in range(max(0, x + i - min_distance), min(self.size, x + i + min_distance + 1)):
                if self.grid[j][y] != "O":
                    return False
        return True

    def place_ship(self, ship):              # размещает корабль на доске.
        max_attempts = 100

        for _ in range(max_attempts):
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)

            if self.is_valid_ship_location(x, y, ship):
                for i in range(ship.size):
                    self.grid[x + i][y] = ship.symbols[i]
                ship.position = [(x + i, y) for i in range(ship.size)]
                self.ships.append(ship)
                break

    def shoot(self, x, y):                 # выстрел по координатам (x, y)
        try:
            if self.grid[x][y] == "X" or self.grid[x][y] == "T":
                print("Вы уже стреляли в эту точку. Попробуйте другую.")
                return False
            elif self.grid[x][y] == "■":
                print("Попадание!")
                self.grid[x][y] = "X"
                return True
            else:
                print("Мимо!")
                self.grid[x][y] = "T"
                return False
        except IndexError:
            print("Ошибка ввода. Пожалуйста, введите числа от 1 до 6.")
            return False

class PlayerBoard(Board):
    pass
                            #Эти классы наследуют от класса Board, расширяя его функциональность
class AIBoard(Board):
    pass

class BattleshipGame:                             #Этот класс управляет общей логикой игры
    """Этот класс управляет общей логикой игры. У него есть методы для размещения кораблей,
    обработки ходов игрока и ИИ, проверки завершения игры, вывода победителя и выполнения самой игры."""

    def __init__(self, board_size, num_ships):
        self.player_board = PlayerBoard(board_size) #инициализация PlayerBoard
        self.ai_board = AIBoard(board_size)   #инициализация  AIBoard
        self.turns = 0                      #инициализация ходов
        self.ai_moves = set()               # инициализация и запись ходов ии

    def place_ships(self):                   #размещение кораблей на досках игрока и ИИ
        ship_sizes = [3, 2, 2, 1, 1, 1, 1]   #размеры кораблей
        for size in ship_sizes:
            player_ship = Ship(size)
            ai_ship = Ship(size)
            self.player_board.place_ship(player_ship)
            self.ai_board.place_ship(ai_ship)

    def print_boards(self):                 #вывод текущего состояния досок игрока и ИИ
        print("Ваша доска:")
        self.player_board.print_board()
        print("\nДоска противника:")
        self.ai_board.print_board()

    def player_turn(self):                #обработка хода игрока
        print("Ваш ход:")
        self.print_boards()

        while True:
            try:
                guess_x = int(input("Введите номер строки (1-6): ")) - 1
                guess_y = int(input("Введите номер столбца (1-6): ")) - 1

                if 0 <= guess_x < self.ai_board.size and 0 <= guess_y < self.ai_board.size:
                    if self.ai_board.grid[guess_x][guess_y] == "X" or self.ai_board.grid[guess_x][guess_y] == "T":
                        print("Вы уже стреляли в эту точку. Попробуйте другую.")
                        continue
                    hit = self.ai_board.shoot(guess_x, guess_y)
                    break
                else:
                    print("Ошибка ввода. Пожалуйста, введите числа от 1 до 6.")
            except ValueError:
                print("Ошибка ввода. Пожалуйста, введите числа от 1 до 6.")

        if hit and all(ship.is_sunk for ship in self.ai_board.ships):
            self.print_game_over("player")
            return True

        return False

    def ai_turn(self):            # симуляция хода ИИ
        print("Ход противника:")
        available_moves = [(x, y) for x in range(self.player_board.size) for y in range(self.player_board.size) if (x, y) not in self.ai_moves]

        if not available_moves:
            print("ИИ больше не может сделать ходы. Игра окончена.")
            return

        guess_x, guess_y = random.choice(available_moves)
        self.ai_moves.add((guess_x, guess_y))

        print(f"ИИ выбрал координаты: ({guess_x+1}, {guess_y+1})")  # Добавлен вывод координат

        self.player_board.shoot(guess_x, guess_y)

        if all(ship.is_sunk for ship in self.player_board.ships):
            self.print_game_over("ai")
            return True

        return False

    def is_game_over(self):           #проверка завершения игры
        return all(ship.is_sunk for ship in self.ai_board.ships) or all(ship.is_sunk for ship in self.player_board.ships) or \
               all(symbol != "■" for row in self.ai_board.grid for symbol in row) or \
               all(symbol != "■" for row in self.player_board.grid for symbol in row)

    def print_winner(self, winner):     #вывод победителя игры
        if all(symbol != "■" for row in self.ai_board.grid for symbol in row):
            print(f"Поздравляем! Вы потопили все корабли противника за {self.turns} ходов.")
        elif all(symbol != "■" for row in self.player_board.grid for symbol in row):
            print(f"Противник потопил все ваши корабли за {self.turns} ходов. Игра окончена.")
        else:
            print("Игра завершилась, но никто не победил.")

    def play(self):                  #главный цикл игры
        self.place_ships()

        current_player = "player"

        while not self.is_game_over():
            if current_player == "player":
                player_hit = self.player_turn()
                current_player = "ai"
            else:
                ai_hit = self.ai_turn()
                current_player = "player"

            self.turns += 1

        winner = "player" if all(ship.is_sunk for ship in self.ai_board.ships) else "ai"
        self.print_winner(winner)

if __name__ == "__main__":
    game = BattleshipGame(board_size=6, num_ships=7)
    game.play()





































