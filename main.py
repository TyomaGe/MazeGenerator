from random import random
from drawer import MazeDrawer
from maze import MazeGenerator


if __name__ == "__main__":
    seed = random()
    maze_generator = MazeGenerator()
    maze = maze_generator.generate(35, 35, start=(0, 0), seed=2025, shortcut_coef=0.15)
    drawer = MazeDrawer(maze, cell_size=12)
    drawer.draw()
