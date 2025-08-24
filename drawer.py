import pygame
from enum import Enum
from shaper import CellType


class MazeDrawer:
    def __init__(self, matrix, cell_size=40):
        self.__matrix = matrix
        self.__cell_size = cell_size
        self.__rows = len(matrix)
        self.__cols = len(matrix[0])
        self.__palette = {
            CellType.WALL: Color.GRAY,
            CellType.EMPTY: Color.WHITE,
            CellType.START: Color.GREEN
        }
        pygame.init()
        self.__screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
        self.__screen.fill(Color.BLACK)
        pygame.display.set_caption("Лабиринт")

    def __draw_maze(self):
        maze_width = self.__cols * self.__cell_size
        maze_height = self.__rows * self.__cell_size
        off_x = (self.__screen.get_width() - maze_width) // 2
        off_y = (self.__screen.get_height() - maze_height) // 2
        for y, row in enumerate(self.__matrix):
            for x, cell in enumerate(row):
                rect = pygame.Rect(
                    off_x + x * self.__cell_size,
                    off_y + y * self.__cell_size,
                    self.__cell_size,
                    self.__cell_size
                )
                color = self.__palette[cell]
                pygame.draw.rect(self.__screen, color, rect)
        pygame.display.flip()

    def draw(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.__screen = pygame.display.set_mode(
                        event.size,
                        pygame.RESIZABLE
                    )
            self.__draw_maze()
            clock.tick(60)
        pygame.quit()


class Color(tuple, Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (64, 64, 64)
    GREEN = (0, 128, 0)
    RED = (255, 0, 0)