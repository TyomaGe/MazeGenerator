import pygame
from enum import Enum


class MazeDrawer:
    def __init__(self, matrix, cell_size=40):
        self._matrix = matrix
        self._cell_size = cell_size
        self._rows = len(matrix)
        self._cols = len(matrix[0])
        self._palette = {
            True: Color.GRAY,
            False: Color.WHITE
        }
        pygame.init()
        self._screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
        self._screen.fill(Color.BLACK)
        pygame.display.set_caption("Лабиринт")

    def _draw_maze(self):
        maze_width = self._cols * self._cell_size
        maze_height = self._rows * self._cell_size
        off_x = (self._screen.get_width() - maze_width) // 2
        off_y = (self._screen.get_height() - maze_height) // 2
        for y, row in enumerate(self._matrix):
            for x, cell in enumerate(row):
                rect = pygame.Rect(
                    off_x + x * self._cell_size,
                    off_y + y * self._cell_size,
                    self._cell_size,
                    self._cell_size
                )
                color = self._palette[cell]
                pygame.draw.rect(self._screen, color, rect)
        pygame.display.flip()

    def draw(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    self._screen = pygame.display.set_mode(
                        event.size,
                        pygame.RESIZABLE
                    )
            self._draw_maze()
            clock.tick(60)
        pygame.quit()


class Color(tuple, Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (64, 64, 64)
    GREEN = (0, 128, 0)
    RED = (255, 0, 0)