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
    _DIRECTIONS = [
        Directions.UP,
        Directions.DOWN,
        Directions.LEFT,
        Directions.RIGHT
    ]

    def __init__(self):
       self._maze = None
       self._lwidth = None
       self._lheight = None
       self._rwidth = None
       self._rheight = None

    def _rmap(self, coordinate):
        return coordinate * 2 + 1

    def _rpmap(self, point):
        return point[0] * 2 + 1, point[1] * 2 + 1

    def _connect(self, f_point, s_point):
        rmap = self._rmap
        fx, fy = f_point
        sx, sy = s_point
        dx, dy = sx - fx, sy - fy
        self._maze.empty((rmap(fx) + dx, rmap(fy) + dy))
        self._maze.empty(self._rpmap(s_point))

    def _set_start(self, start):
        self._maze.empty(self._rpmap(start))

    def _is_inside(self, point):
        x, y = point
        return 0 <= x < self._lwidth and 0 <= y < self._lheight

    def _is_connectable(self, neighbour):
        rneighbour = self._rpmap(neighbour)
        return self._is_inside(neighbour) and self._maze.is_wall(rneighbour)

    def _get_neighbour(self, current, direction):
        return current[0] + direction[0], current[1] + direction[1]

    def generate(self, lwidth, lheight, start=(0, 0), seed=0, shortcut_coef=0.0):
        self._lwidth = lwidth
        self._lheight = lheight
        self._rwidth = self._rmap(lwidth)
        self._rheight = self._rmap(lheight)
        self._maze = Maze(self._rwidth, self._rheight)
        random.seed(seed)
        self._set_start(start)
        stack = [start]
        while stack:
            current = stack[-1]
            random.shuffle(self._DIRECTIONS)
            moved = False
            for direction in self._DIRECTIONS:
                neighbor = self._get_neighbour(current, direction)
                if self._is_connectable(neighbor):
                    self._connect(current, neighbor)
                    stack.append(neighbor)
                    moved = True
                    break
            if not moved:
                stack.pop()
        self.add_shortcuts(shortcut_coef)
        return self._maze.get_maze()

    def add_shortcuts(self, shortcut_coef):
        if shortcut_coef <= 0.0:
            return
        is_deletable = self._is_deletable
        is_wall = self._maze.is_wall
        check_fn = is_deletable if shortcut_coef < 0.75 else is_wall
        candidates = []
        for y in range(1, self._maze.height - 1):
            for x in range(1, self._maze.width - 1):
                point = (x, y)
                if check_fn(point):
                    candidates.append(point)
        random.shuffle(candidates)
        shortcuts_target = int(len(candidates) * shortcut_coef)
        for i in range(min(shortcuts_target, len(candidates))):
            self._maze.empty(candidates[i])

    def _is_deletable(self, point):
        if self._maze.is_empty(point):
            return False
        x, y = point
        left = self._maze.is_wall((x - 1, y))
        right = self._maze.is_wall((x + 1, y))
        up = self._maze.is_wall((x, y - 1))
        down = self._maze.is_wall((x, y + 1))
        is_corner = (up or down) and (right or left)
        return not is_corner
