from random import random
from drawer import MazeDrawer
from maze import MazeGenerator


if __name__ == "__main__":
    seed = random()
    maze_generator = MazeGenerator()
    maze = maze_generator.generate(15, 15, finish=(14, 14), seed=seed, shortcut_coef=0.05)
    drawer = MazeDrawer(maze, cell_size=15)
    drawer.draw()
