import random
from enum import Enum


class MazeShaper:
    class __Directions(tuple, Enum):
        LEFT = (-1, 0)
        RIGHT = (1, 0)
        UP = (0, 1)
        DOWN = (0, -1)

    __DIRECTIONS = [__Directions.UP, __Directions.DOWN,
                    __Directions.LEFT, __Directions.RIGHT
                    ]

    def __init__(self, width=10, height=10, seed=0):
        self.__width = width // 2
        self.__height = height // 2
        random.seed(seed) # фиксирует начальное состояние генератора случайных чисел, для одинаковых сидов будет всегда один и тот же лабиринт
        self.__maze = [[CellType.WALL for _ in range(coord(self.__width))]
                       for _ in range(coord(self.__height))]

    def generate(self, entry=(0, 0), gaps_chance=0.0): # возможно стоит и конечную точку задать
        sx, sy = entry # стартовая клетка
        self.__maze[coord(sy)][coord(sx)] = CellType.START # замени на .EMPTY, это я для себя START сделал
        stack = [(sx, sy)]
        while stack:
            x, y = stack[-1] # верхний элемент стека
            random.shuffle(self.__DIRECTIONS)
            moved = False
            for direction in self.__DIRECTIONS:
                dx, dy = direction # направление куда будем идти
                nx, ny = x + dx, y + dy # новая соседняя клетка в которую пришли
                if (0 <= nx < self.__width and 0 <= ny < self.__height # проверка на границы
                        and self.__maze[coord(ny)][coord(nx)] == CellType.WALL): # проверка на непосещённость
                    self.__maze[coord(y) + dy][coord(x) + dx] = CellType.EMPTY # делаем пустой стену между клетками
                    self.__maze[coord(ny)][coord(nx)] = CellType.EMPTY # делаем пустой соседнюю клетку
                    stack.append((nx, ny))
                    moved = True
                    break
            if not moved:
                stack.pop()

        ex, ey = self.__width - 1, self.__height - 1 # выход
        self.__maze[coord(ey)][coord(ex)] = CellType.EMPTY
        self.__maze[coord(ey)][coord(ex) + 1] = CellType.EMPTY
        self.__add_gaps(gaps_chance) # делаем дырки между проходами
        return self.__maze

    def __add_gaps(self, gaps_chance):
        """
        Добавляем случайные проходы в стены
        """
        candidates = [] # стены, которые можно безопасно превратить в проход
        for y in range(1, len(self.__maze) - 1): # идем по внутренней части матрицы
            for x in range(1, len(self.__maze[0]) - 1):
                if self.__maze[y][x] == CellType.WALL and self.__can_be_shortcut(x, y):
                    candidates.append((x, y)) # если кандидат прошел проверку на __can_be_shortcut, то добавляем его в список
        random.shuffle(candidates) # перемешаем кандидатов
        shortcuts_target = int(len(candidates) * gaps_chance) # целевое количество дыр
        for i in range(min(shortcuts_target, len(candidates))): # выберем первых сколько-то там из них
            # random.shuffle(candidates) # можно еще больше рандома добавить
            x, y = candidates[i]
            self.__maze[y][x] = CellType.EMPTY # и продырявим))

    def __can_be_shortcut(self, x, y):
        """
        Проверяет, можно ли превратить эту стену в проход:
        должна соединять две пустые клетки слева-справа или сверху-снизу
        """
        if self.__maze[y][x] != CellType.WALL:
            return False
        left = self.__maze[y][x - 1] == CellType.EMPTY # проверка справа слева пустые или нет
        right = self.__maze[y][x + 1] == CellType.EMPTY
        if left and right:
            return True
        up = self.__maze[y - 1][x] == CellType.EMPTY # проверка сверху снизу пустые или нет
        down = self.__maze[y + 1][x] == CellType.EMPTY
        if up and down:
            return True
        return False


class CellType(str, Enum):
    WALL = 'W'
    EMPTY = '.'
    START = "S"


def coord(position):
    """
    Логическая сетка у нас height x width клеток
    Но мы хотим делать стены между клетками и стены снаружи

    Пример
    ◯ ◯ ◯  если у нас была ширина 3
    █ ◯ █ ◯ █ ◯ █  то теперь будет 7
    В алгоритме мы будем ломать эти стены

    Эта функция будет вычислять координаты с учетом этих стенок
    """
    return position * 2 + 1
