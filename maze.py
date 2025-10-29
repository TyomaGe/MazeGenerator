import random
import numpy as np
from enum import Enum


class Directions(tuple, Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)


class Maze:
    def __init__(self, width, height):
        self.__maze = np.ones((height, width), dtype=bool)
        self.__width = width
        self.__height = height

    def empty(self, point):
        self.__maze[point[1], point[0]] = False

    def wall(self, point):
        self.__maze[point[1], point[0]] = True

    def is_wall(self, point):
        return self.__maze[point[1], point[0]]

    def is_empty(self, point):
        return not self.__maze[point[1], point[0]]

    def get_maze(self):
        return self.__maze.tolist()

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height


class MazeGenerator:
    __DIRECTIONS = [
        Directions.UP,
        Directions.DOWN,
        Directions.LEFT,
        Directions.RIGHT
    ]

    def __init__(self):
       self.__maze = None
       self.__lwidth = None
       self.__lheight = None
       self.__rwidth = None
       self.__rheight = None

    def __rmap(self, coordinate):
        return coordinate * 2 + 1

    def __rpmap(self, point):
        return point[0] * 2 + 1, point[1] * 2 + 1

    def __connect(self, f_point, s_point):
        rmap = self.__rmap
        fx, fy = f_point
        sx, sy = s_point
        dx, dy = sx - fx, sy - fy
        self.__maze.empty((rmap(fx) + dx, rmap(fy) + dy))
        self.__maze.empty(self.__rpmap(s_point))

    def __set_start(self, start):
        self.__maze.empty(self.__rpmap(start))

    def __is_inside(self, point):
        x, y = point
        return 0 <= x < self.__lwidth and 0 <= y < self.__lheight

    def __is_connectable(self, neighbour):
        rneighbour = self.__rpmap(neighbour)
        return self.__is_inside(neighbour) and self.__maze.is_wall(rneighbour)

    def __get_neighbour(self, current, direction):
        return current[0] + direction[0], current[1] + direction[1]

    def generate(self, lwidth, lheight, start=(0, 0), seed=0, shortcut_coef=0.0):
        self.__lwidth = lwidth
        self.__lheight = lheight
        self.__rwidth = self.__rmap(lwidth)
        self.__rheight = self.__rmap(lheight)
        self.__maze = Maze(self.__rwidth, self.__rheight)
        random.seed(seed)
        self.__set_start(start)
        stack = [start]
        while stack:
            current = stack[-1]
            random.shuffle(self.__DIRECTIONS)
            moved = False
            for direction in self.__DIRECTIONS:
                neighbor = self.__get_neighbour(current, direction)
                if self.__is_connectable(neighbor):
                    self.__connect(current, neighbor)
                    stack.append(neighbor)
                    moved = True
                    break
            if not moved:
                stack.pop()
        self.__add_shortcuts(shortcut_coef)
        return self.__maze.get_maze()

    def __add_shortcuts(self, shortcut_coef):
        if shortcut_coef <= 0.0:
            return
        is_deletable = self.__is_deletable
        is_wall = self.__maze.is_wall
        check_fn = is_deletable if shortcut_coef < 0.75 else is_wall
        candidates = []
        for y in range(1, self.__maze.height - 1):
            for x in range(1, self.__maze.width - 1):
                point = (x, y)
                if check_fn(point):
                    candidates.append(point)
        random.shuffle(candidates)
        shortcuts_target = int(len(candidates) * shortcut_coef)
        for i in range(min(shortcuts_target, len(candidates))):
            self.__maze.empty(candidates[i])

    def __is_deletable(self, point):
        if self.__maze.is_empty(point):
            return False
        x, y = point
        left = self.__maze.is_wall((x - 1, y))
        right = self.__maze.is_wall((x + 1, y))
        up = self.__maze.is_wall((x, y - 1))
        down = self.__maze.is_wall((x, y + 1))
        is_corner = (up or down) and (right or left)
        return not is_corner
